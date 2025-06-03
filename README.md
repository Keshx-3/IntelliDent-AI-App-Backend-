# 🦷 IntelliDent AI - FastAPI Backend

IntelliDent AI is a cloud-powered dental assistant backend built with FastAPI. It handles:

- User authentication and profile management
- Doctor listings and appointments
- Product orders
- Dental scan uploads (analyzed by Gemini AI)
- Auto-generated PDF dental reports

---

## 🚀 Features

- ✅ JWT-based Authentication (Login, Register, Update Profile)
- ✅ Scan Uploads & AI Diagnosis (via Gemini 1.5 Flash)
- ✅ PDF Dental Report Generation using docx + docx2pdf
- ✅ Admin and User roles
- ✅ Order management & doctor lookup
- ✅ Hosted on AWS EC2 (with Elastic IP + HTTPS ready setup)

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/<your-username>/IntelliDent-AI-App.git
cd IntelliDent-AI-App

# Setup environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
