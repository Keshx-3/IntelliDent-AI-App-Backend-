from datetime import datetime, date
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from jose import jwt, JWTError
from db import get_connection
from utils.token import oauth2_scheme
from auth import SECRET_KEY, ALGORITHM
from dotenv import load_dotenv
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
from docx2pdf import convert
from PIL import Image as PILImage
from io import BytesIO
import os
import ast
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

router = APIRouter(prefix="/scans", tags=["Scan Management"])

TEMPLATE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates", "scan_report_template.docx"))
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

CLINICAL_PROMPT = """You are to act as a highly experienced and formally trained dentist with over fifty years of distinguished clinical practice in diagnosing and treating a wide range of dental conditions. When an image is uploaded, examine it thoroughly and deliver a precise, professional diagnosis of any identifiable dental condition. Following the diagnosis, provide an in-depth explanation of the condition in clear, clinical yet comprehensible language.
Based on the image, assess and state the potential severity of the condition as a percentage. You must state the severity directly in numeric form such as 85%, and refrain from using phrases such as 'it's difficult to give an exact percentage without further clinical examination'. Your assessment must be image-based and precise.
Next, present practical, evidence-based home remedies or temporary interventions that may offer relief until formal dental consultation is obtained. Then, provide dietary recommendations or food-based solutions that may contribute to the management or prevention of the condition.
Finally, issue a professional and appropriate call for action based on the observed severity — clearly advising whether the individual should seek immediate dental attention or may monitor the situation with care.
All responses must be extremely formal, medically sound, and must follow the exact structured format below. Use these exact headings (clearly separated) in the output and provide corresponding detailed information under each heading:
Dental Condition Name
[Provide the name of the dental condition]
Information About the Condition
[Give a formal, medically accurate explanation of the condition in detail]
Severity Percentage
[State the danger or severity level clearly as a number, such as 72%]
Home Cure or Remedy
[Recommend effective and safe home-based solutions to alleviate symptoms temporarily]
Dietary Options or Food Solutions
[Suggest food items or dietary adjustments that support oral health related to the diagnosed condition]
Call for Action
[Formally advise whether the user must see a dentist urgently or continue monitoring, based on the severity]
Speak as if addressing a real patient in a clinical setting, not as a chatbot. Your language must reflect deep clinical expertise, compassion, and clarity. Do not use informal language, markdown, bullet points, symbols, or AI disclaimers. Your response must always reflect the communication style of a senior dental consultant who has spent a lifetime in clinical care.
"""

def calculate_age(dob_str):
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    except:
        return "N/A"

def safe_list(value):
    if isinstance(value, str):
        try:
            parsed = ast.literal_eval(value)
            return parsed if isinstance(parsed, list) else [value]
        except:
            return [value]
    elif isinstance(value, list):
        return value
    else:
        return [str(value)]

@router.post("/")
async def analyze_scan(files: List[UploadFile] = File(...), token: str = Depends(oauth2_scheme)):
    converted_image_paths = []
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Fetch user
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Validate and convert uploaded images
        image_parts = []
        for file in files:
            content = await file.read()
            try:
                img = PILImage.open(BytesIO(content))
                converted_path = os.path.join(REPORTS_DIR, f"converted_{datetime.utcnow().timestamp()}.png")
                img.convert("RGB").save(converted_path, format="PNG")
                image_parts.append({
                    "mime_type": "image/png",
                    "data": open(converted_path, "rb").read()
                })
                converted_image_paths.append(converted_path)
            except Exception as e:
                print(f"[ERROR] Invalid image '{file.filename}':", str(e))

        if not converted_image_paths:
            raise HTTPException(status_code=400, detail="No valid image files uploaded.")

        # AI Diagnosis
        full_text = ""
        for idx, part in enumerate(image_parts):
            response = model.generate_content([CLINICAL_PROMPT, part])
            full_text += f"\n--- Analysis for Image {idx + 1} ---\n{response.text.strip()}\n"

        # Parse response
        sections = {
            "Dental Condition Name": "",
            "Information About the Condition": "",
            "Severity Percentage": "",
            "Home Cure or Remedy": "",
            "Dietary Options or Food Solutions": "",
            "Call for Action": ""
        }
        current = None
        for line in full_text.splitlines():
            line = line.strip()
            if not line:
                continue
            if line in sections:
                current = line
            elif current:
                sections[current] += line + " "

        # Fill context
        age = calculate_age(str(user.get("date_of_birth")))
        context = {
            "first_name": user.get("first_name"),
            "last_name": user.get("last_name"),
            "email": user.get("email"),
            "gender": user.get("gender", "N/A"),
            "date_of_birth": str(user.get("date_of_birth")),
            "age": age,
            "contact_number": user.get("contact_number", "N/A"),
            "address": user.get("address", "N/A"),
            "symptoms": ", ".join(safe_list(user.get("symptoms"))),
            "previous_treatments": ", ".join(safe_list(user.get("previous_treatments"))),
            "brushing_frequency": user.get("brushing_frequency", "N/A"),
            "tobacco_use": "Yes" if str(user.get("tobacco_use", "")).lower() in ["1", "true", "yes"] else "No",
            "condition": sections["Dental Condition Name"].strip(),
            "severity": sections["Severity Percentage"].strip(),
            "info": sections["Information About the Condition"].strip(),
            "remedy": sections["Home Cure or Remedy"].strip(),
            "diet": sections["Dietary Options or Food Solutions"].strip(),
            "action": sections["Call for Action"].strip(),
        }

        # Prepare template and image placeholders
        doc = DocxTemplate(TEMPLATE_PATH)
        for i in range(5):
            key = f"image_{i + 1}"
            if i < len(converted_image_paths):
                context[key] = InlineImage(doc, converted_image_paths[i], width=Inches(2))
            else:
                context[key] = ""

        # Save DOCX and convert to PDF
        timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        docx_name = f"{email.replace('@', '_')}_{timestamp}.docx"
        pdf_name = docx_name.replace(".docx", ".pdf")
        docx_path = os.path.join(REPORTS_DIR, docx_name)
        pdf_path = os.path.join(REPORTS_DIR, pdf_name)

        doc.render(context)
        doc.save(docx_path)
        convert(docx_path, pdf_path)
        os.remove(docx_path)  # <- this will delete the .docx file after PDF is created

        # Clean up temporary images
        for path in converted_image_paths:
            try:
                os.remove(path)
            except:
                pass

        public_ip = os.getenv("PUBLIC_SERVER_IP", "127.0.0.1")
        report_url = f"http://{public_ip}:8000/reports/{pdf_name}"

        return {
            "email": email,
            "pdf_url": report_url,
            "analysis": {
                "condition": context["condition"],
                "severity": context["severity"],
                "action": context["action"]
            }
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
