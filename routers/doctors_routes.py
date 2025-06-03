from fastapi import APIRouter, HTTPException, Depends
from db import get_connection
from schemas import DoctorOut
from utils.token import oauth2_scheme
from utils.roles import require_admin

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("/", response_model=list[DoctorOut])
def list_doctors():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    cursor.close()
    conn.close()
    return doctors

@router.get("/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM doctors WHERE id = %s", (doctor_id,))
    doctor = cursor.fetchone()
    cursor.close()
    conn.close()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

# ✅ Admin-only: Add doctor
@router.post("/")
def add_doctor(data: dict, token: str = Depends(oauth2_scheme)):
    require_admin(token)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO doctors (first_name, last_name, short_bio, gender, specialty, languages, rating, profile_image, city)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data["first_name"], data["last_name"], data.get("short_bio"),
        data.get("gender"), data.get("specialty"), data.get("languages"),
        data.get("rating"), data.get("profile_image"), data.get("city")
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Doctor added successfully"}

# ✅ Admin-only: Edit doctor
@router.put("/{doctor_id}")
def update_doctor(doctor_id: int, data: dict, token: str = Depends(oauth2_scheme)):
    require_admin(token)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE doctors SET first_name=%s, last_name=%s, short_bio=%s, gender=%s,
        specialty=%s, languages=%s, rating=%s, profile_image=%s, city=%s
        WHERE id=%s
    """, (
        data["first_name"], data["last_name"], data.get("short_bio"),
        data.get("gender"), data.get("specialty"), data.get("languages"),
        data.get("rating"), data.get("profile_image"), data.get("city"), doctor_id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Doctor updated successfully"}

# ✅ Admin-only: Delete doctor
@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, token: str = Depends(oauth2_scheme)):
    require_admin(token)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM doctors WHERE id = %s", (doctor_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Doctor deleted successfully"}
