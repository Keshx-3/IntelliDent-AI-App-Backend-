from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from db import get_connection
from utils.token import oauth2_scheme
from jose import jwt, JWTError
from auth import SECRET_KEY, ALGORITHM
from datetime import datetime
from schemas import StatusUpdate
from utils.roles import require_admin

router = APIRouter(prefix="/appointments", tags=["Appointments"])

class AppointmentRequest(BaseModel):
    doctor_id: int
    appointment_time: datetime

@router.post("/")
def book_appointment(data: AppointmentRequest, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        cursor.execute("SELECT id FROM doctors WHERE id=%s", (data.doctor_id,))
        doctor = cursor.fetchone()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        cursor.execute("""
            INSERT INTO appointments (user_id, doctor_id, appointment_time, status)
            VALUES (%s, %s, %s, 'pending')
        """, (user["id"], data.doctor_id, data.appointment_time))
        conn.commit()

        return {"message": "Appointment booked successfully"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    finally:
        cursor.close()
        conn.close()


@router.get("/")
def get_appointments(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM users WHERE email=%s", (user_email,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        cursor.execute("""
            SELECT 
                a.id, a.doctor_id, a.appointment_time, a.status,
                CONCAT(d.first_name, ' ', d.last_name) AS doctor_name,
                d.specialty
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            WHERE a.user_id = %s
        """, (user["id"],))
        appointments = cursor.fetchall()

        return {"appointments": appointments}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    finally:
        cursor.close()
        conn.close()

@router.put("/{appointment_id}/status")
def update_appointment_status(appointment_id: int, status_update: StatusUpdate, token: str = Depends(oauth2_scheme)):
    require_admin(token)

    conn = get_connection()
    cursor = conn.cursor()

    # Optionally: validate status value
    valid_statuses = ["pending", "confirmed", "completed", "cancelled"]
    if status_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")

    cursor.execute("UPDATE appointments SET status = %s WHERE id = %s", (status_update.status, appointment_id))
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": f"Appointment status updated to '{status_update.status}'"}
