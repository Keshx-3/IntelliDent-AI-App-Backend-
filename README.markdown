# 🦷 🦷 IntelliDent AI - FastAPI Backend

This is a dental clinic management and diagnostics platform built with FastAPI, offering user authentication, AI-driven dental scan analysis, doctor and appointment management, product catalog, and order processing.

## 🚀 Features
- **User Authentication & Profile Management**: Secure registration, login, profile updates, and avatar uploads.
- **AI-Based Dental Scan Analysis**: Upload dental images for AI diagnosis with PDF report generation.
- **Doctor Listings & Appointment Scheduling**: Browse doctors and book appointments.
- **Product Catalog & Order Management**: View and order dental products.
- **Secure Deployment**: Deploy with Nginx, Certbot, and systemd for reliability.

## 🛠️ Tech Stack
- **FastAPI**: High-performance API framework.
- **MySQL**: Database for user, doctor, appointment, and order data.
- **Gemini 1.5 (Google Generative AI)**: Powers AI dental scan analysis.
- **DocxTemplate + docx2pdf**: Generates PDF reports for scan results.
- **PIL (Pillow)**: Handles image processing for dental scans.
- **Uvicorn**: ASGI server for running FastAPI.
- **Nginx + Certbot**: Ensures secure HTTPS deployment.

## 📚 API Endpoints

### 🔐 Authentication

#### POST /auth/register
**Purpose**: Registers a new user.  
**Input**:  
- Body (JSON):
  ```json
  {
    "email": "testuser@example.com",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }
  ```  
**Output**:  
- Success: HTTP 200 with user creation confirmation.
- Error: HTTP 400 if email exists or input is invalid.

#### POST /auth/token
**Purpose**: Logs in a user and returns a JWT token.  
**Input**:  
- Body (x-www-form-urlencoded):
  ```
  username=testuser@example.com
  password=testpass123
  ```  
**Output**:  
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5c...",
    "token_type": "bearer"
  }
  ```  
**Note**: Use the `access_token` as a Bearer token in the `Authorization` header for protected endpoints.

#### GET /auth/me
**Purpose**: Retrieves the current user's profile.  
**Input**:  
- Header:
  ```
  Authorization: Bearer <your_token_here>
  ```  
**Output**:  
- Success: HTTP 200 with user details (e.g., email, first_name, last_name).
- Error: HTTP 401 if token is invalid or missing.

#### PUT /auth/update
**Purpose**: Updates the current user's profile.  
**Input**:  
- Header:
  ```
  Authorization: Bearer <your_token_here>
  ```  
- Body (JSON):
  ```json
  {
    "gender": "M",
    "date_of_birth": "2000-01-01T00:00:00",
    "under_physician_care": true,
    "chronic_conditions": false,
    "any_allergies": false,
    "under_medications": false,
    "pregnant_or_nursing": false,
    "symptoms": ["tooth_pain"],
    "previous_treatments": ["root_canal"],
    "diagnosed_gum_disease": false,
    "brushing_frequency": "Twice daily",
    "flossing": true,
    "tobacco_use": false,
    "sugary_diet": true,
    "teeth_grinding": false,
    "is_subscribed": true
  }
  ```  
**Output**:  
- Success: HTTP 200 with updated profile details.
- Error: HTTP 400 for invalid input or HTTP 401 for unauthorized access.

### 👤 User Profile

#### GET /profile/
**Purpose**: Retrieves the current user's profile (similar to `/auth/me`).  
**Input**:  
- Header:
  ```
  Authorization: Bearer <your_token_here>
  ```  
**Output**:  
- Success: HTTP 200 with user profile details.
- Error: HTTP 401 if token is invalid or missing.

#### PUT /profile/
**Purpose**: Updates the current user's profile (alternative to `/auth/update`).  
**Input**:  
- Header:
  ```
  Authorization: Bearer <your_token_here>
  ```  
- Body (JSON): Same as `/auth/update`.  
**Output**:  
- Success: HTTP 200 with updated profile details.
- Error: HTTP 400 for invalid input or HTTP 401 for unauthorized access.

#### POST /profile/avatar
**Purpose**: Uploads a profile avatar.  
**Input**:  
- Header:
  ```
  Authorization: Bearer <your_token_here>
  ```  
- Body: Multipart form data with `avatar=<file>`.  
**Output**:  
- Success: HTTP 200 with upload confirmation.
- Error: HTTP 400 for invalid file or HTTP 401 for unauthorized access.

#### GET /profile/scans
**Purpose**: Retrieves the user's AI scan history.  
**Input**:  
- Header:
  ```
  Authorization: Bearer <your_token_here>
  ```  
**Output**:  
- Success: HTTP 200 with a list of scan records.
- Error: HTTP 401 if token is invalid or missing.

### 🧠 AI Scan Analysis

#### POST /scans/
**Purpose**: Uploads up to 5 dental images for AI analysis and generates a PDF report.  
**Input**:  
- Header:
  ```
  Authorization: Bearer <your_token_here>
  ```  
- Body: Multipart form data with `files=[image1.png, image2.jpg, ...]`.  
**Output**:  
  ```json
  {
    "email": "testuser@example.com",
    "pdf_url": "http://your-server/reports/user_2025-05-31_13-22-01.pdf",
    "analysis": {
      "condition": "Gingivitis",
      "severity": "70%",
      "action": "Immediate dental consultation advised"
    }
  }
  ```  
- Error: HTTP 400 for invalid files or HTTP 401 for unauthorized access.

### 🧑‍⚕️ Doctors

#### GET /doctors/
**Purpose**: Lists all available doctors.  
**Input**: None.  
**Output**:  
- Success: HTTP 200 with a list of doctors (e.g., id, name, specialty).
- Error: HTTP 500 for server issues.

#### GET /doctors/{doctor_id}
**Purpose**: Retrieves details of a specific doctor.  
**Input**:  
- URL Parameter: `doctor_id` (e.g., `/doctors/1`).  
**Output**:  
- Success: HTTP 200 with doctor details (e.g., name, specialty).
- Error: HTTP 404 if doctor_id is not found.

### 📅 Appointments

#### POST /appointments/
**Purpose**: Books a new appointment.  
**Input**:  
- Header:
  ```
  Authorization: Bearer <your_token_here>
  ```  
- Body (JSON):
  ```json
  {
    "doctor_id": 1,
    "appointment_time": "2025-05-20T10:00:00"
  }
  ```  
**Output**:  
- Success: HTTP 200 with appointment confirmation.
- Error: HTTP 400 for invalid input or HTTP 401 for unauthorized access.

#### GET /appointments/
**Purpose**: Retrieves the user's appointments.  
**Input**:  
- Header:
  ```
  Authorization: Bearer <your_token_here>
  ```  
**Output**:  
  ```json
  {
    "appointments": [
      {
        "id": 1,
        "doctor_id": 1,
        "appointment_time": "2025-05-20T10:00:00",
        "status": "pending",
        "doctor_name": "John Doe",
        "specialty": "General Dentistry"
      }
    ]
  }
  ```  
- Error: HTTP 401 if token is invalid or missing.

### 🛒 Products

#### GET /products/
**Purpose**: Lists all available products.  
**Input**: None.  
**Output**:  
- Success: HTTP 200 with a list of products (e.g., id, name, price).
- Error: HTTP 500 for server issues.

#### GET /products/{product_id}
**Purpose**: Retrieves details of a specific product.  
**Input**:  
- URL Parameter: `product_id` (e.g., `/products/2`).  
**Output**:  
- Success: HTTP 200 with product details (e.g., name, price).
- Error: HTTP 404 if product_id is not found.

### 🛍️ Orders

#### POST /orders/
**Purpose**: Creates a new order.  
**Input**:  
- Header:
  ```
  Authorization: Bearer <your_token_here>
  ```  
- Body (JSON):
  ```json
  {
    "items": [
      { "product_id": 1, "quantity": 2 },
      { "product_id": 2, "quantity": 1 }
    ]
  }
  ```  
**Output**:  
- Success: HTTP 200 with order confirmation.
- Error: HTTP 400 for invalid input or HTTP 401 for unauthorized access.

#### GET /orders/
**Purpose**: Retrieves the user's orders.  
**Input**:  
- Header:
  ```
  Authorization: Bearer <your_token_here>
  ```  
**Output**:  
- Success: HTTP 200 with a list of orders (e.g., order_id, items, total).
- Error: HTTP 401 if token is invalid or missing.

#### GET /orders/{order_id}
**Purpose**: Retrieves details of a specific order.  
**Input**:  
- Header:
  ```
  Authorization: Bearer <your_token_here>
  ```  
- URL Parameter: `order_id` (e.g., `/orders/1`).  
**Output**:  
- Success: HTTP 200 with order details (e.g., items, total).
- Error: HTTP 404 if order_id is not found or HTTP 401 for unauthorized access.

## ⚙️ Deployment
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/dental-clinic-api.git
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Environment Variables**: Configure MySQL credentials, Google API keys, and other settings.
4. **Run the Application**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
5. **Configure Nginx + Certbot**: Set up Nginx as a reverse proxy and use Certbot for HTTPS.
6. **Systemd Service**: Ensure the FastAPI app runs on startup with a systemd service.

### Example Systemd Service File
```ini
[Unit]
Description=FastAPI Dental Clinic Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/dental-clinic-api
ExecStart=/home/ubuntu/dental-clinic-api/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

## 📜 License
This project is licensed under the MIT License.
