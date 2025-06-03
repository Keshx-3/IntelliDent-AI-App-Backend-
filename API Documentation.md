# FastAPI Dental Clinic API Documentation

This README provides an overview of the FastAPI endpoints for a dental clinic application. Each endpoint is described with its purpose, required input, and expected output.

## Authentication

### POST /auth/register
**Purpose**: Registers a new user in the system.  
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
**Expected Output**:  
- Success: HTTP 200 with user creation confirmation (details may vary based on implementation).  
- Error: HTTP 400 if email already exists or invalid input.

---

### POST /auth/token
**Purpose**: Logs in a user and returns a JWT token for authentication.  
**Input**:  
- Body (x-www-form-urlencoded):
```
username=testuser@example.com
password=testpass123
```  
**Expected Output**:  
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5c...",
  "token_type": "bearer"
}
```  
**Note**: Copy the `access_token` and use it as a Bearer token in the `Authorization` header for protected endpoints.

---

### GET /auth/me
**Purpose**: Retrieves the current user's profile information.  
**Input**:  
- Header:
```
Authorization: Bearer <your_token_here>
```  
**Expected Output**:  
- Success: HTTP 200 with user profile details (e.g., email, first_name, last_name, etc.).  
- Error: HTTP 401 if token is invalid or missing.

---

## User Profile

### PUT /auth/update
**Purpose**: Updates the current user's profile details.  
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
**Expected Output**:  
- Success: HTTP 200 with updated profile details.  
- Error: HTTP 400 for invalid input or HTTP 401 for unauthorized access.

---

### GET /profile/
**Purpose**: Retrieves the current user's profile information (similar to `/auth/me`).  
**Input**:  
- Header:
```
Authorization: Bearer <your_token_here>
```  
**Expected Output**:  
- Success: HTTP 200 with user profile details.  
- Error: HTTP 401 if token is invalid or missing.

---

### PUT /profile/
**Purpose**: Updates the current user's profile (alternative to `/auth/update`).  
**Input**:  
- Header:
```
Authorization: Bearer <your_token_here>
```  
- Body (JSON): Same as `/auth/update` body.  
**Expected Output**:  
- Success: HTTP 200 with updated profile details.  
- Error: HTTP 400 for invalid input or HTTP 401 for unauthorized access.

---

### POST /profile/avatar
**Purpose**: Uploads a profile avatar for the current user.  
**Input**:  
- Header:
```
Authorization: Bearer <your_token_here>
```  
- Body: Multipart form data with the image file.  
**Expected Output**:  
- Success: HTTP 200 with confirmation of avatar upload.  
- Error: HTTP 400 for invalid file or HTTP 401 for unauthorized access.

---

### GET /profile/scans
**Purpose**: Retrieves the current user's scan history.  
**Input**:  
- Header:
```
Authorization: Bearer <your_token_here>
```  
**Expected Output**:  
- Success: HTTP 200 with a list of scan records.  
- Error: HTTP 401 if token is invalid or missing.

---

## Doctors

### GET /doctors/
**Purpose**: Lists all available doctors. No authentication required.  
**Input**: None.  
**Expected Output**:  
- Success: HTTP 200 with a list of doctors (e.g., id, name, specialty).  
- Error: HTTP 500 for server issues.

---

### GET /doctors/{doctor_id}
**Purpose**: Retrieves details of a specific doctor by ID.  
**Input**:  
- URL Parameter: `doctor_id` (e.g., `/doctors/1`).  
**Expected Output**:  
- Success: HTTP 200 with doctor details (e.g., name, specialty).  
- Error: HTTP 404 if doctor_id is not found.

---

## Appointments

### POST /appointments/
**Purpose**: Books a new appointment with a doctor.  
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
**Expected Output**:  
- Success: HTTP 200 with appointment confirmation.  
- Error: HTTP 400 for invalid input or HTTP 401 for unauthorized access.

---

### GET /appointments/
**Purpose**: Retrieves the list of the current user's appointments.  
**Input**:  
- Header:
```
Authorization: Bearer <your_token_here>
```  
**Expected Output**:  
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

---

## Products

### GET /products/
**Purpose**: Lists all available products. No authentication required.  
**Input**: None.  
**Expected Output**:  
- Success: HTTP 200 with a list of products (e.g., id, name, price).  
- Error: HTTP 500 for server issues.

---

### GET /products/{product_id}
**Purpose**: Retrieves details of a specific product by ID.  
**Input**:  
- URL Parameter: `product_id` (e.g., `/products/2`).  
**Expected Output**:  
- Success: HTTP 200 with product details (e.g., name, price).  
- Error: HTTP 404 if product_id is not found.

---

## Orders

### POST /orders/
**Purpose**: Creates a new order for the current user.  
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
**Expected Output**:  
- Success: HTTP 200 with order confirmation.  
- Error: HTTP 400 for invalid input or HTTP 401 for unauthorized access.

---

### GET /orders/
**Purpose**: Retrieves the list of the current user's orders.  
**Input**:  
- Header:
```
Authorization: Bearer <your_token_here>
```  
**Expected Output**:  
- Success: HTTP 200 with a list of orders (e.g., order_id, items, total).  
- Error: HTTP 401 if token is invalid or missing.

---

### GET /orders/{order_id}
**Purpose**: Retrieves details of a specific order by ID.  
**Input**:  
- Header:
```
Authorization: Bearer <your_token_here>
```  
- URL Parameter: `order_id` (e.g., `/orders/1`).  
**Expected Output**:  
- Success: HTTP 200 with order details (e.g., items, total).  
- Error: HTTP 404 if order_id is not found or HTTP 401 for unauthorized access.

---

This documentation covers all endpoints for the dental clinic API. Ensure proper authentication for protected routes using the JWT token obtained from `/auth/token`.