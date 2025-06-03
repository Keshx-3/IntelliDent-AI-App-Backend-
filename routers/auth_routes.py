from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from db import get_connection
from auth import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from schemas import RegisterSchema, UpdateUserProfile, UserAdmin, UserPatient
from jose import jwt, JWTError
from utils.token import oauth2_scheme
from datetime import datetime
import json

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(user: RegisterSchema):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pw = hash_password(user.password)
    cursor.execute("""
        INSERT INTO users (email, password_hash, first_name, last_name)
        VALUES (%s, %s, %s, %s)
    """, (user.email, hashed_pw, user.first_name, user.last_name))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User registered successfully"}


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (form_data.username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user["email"]}, role=user["role"])
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserAdmin | UserPatient)
def get_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        role = payload.get("role")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if role == "admin":
            return UserAdmin(**user)

        # Load JSON fields for normal users
        for key in ["symptoms", "previous_treatments"]:
            if user.get(key):
                try:
                    user[key] = json.loads(user[key])
                except:
                    user[key] = []

        return UserPatient(**user)

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.put("/update")
def update_user(data: UpdateUserProfile, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        fields, values = [], []

        for field, value in data.dict(exclude_unset=True).items():
            if field in ["symptoms", "previous_treatments"]:
                fields.append(f"{field} = %s")
                values.append(json.dumps(value))
            elif field == "brushing_frequency":
                if value not in ['Once daily', 'Twice daily', 'Occasionally', 'Rarely']:
                    continue
                fields.append(f"{field} = %s")
                values.append(value)
            elif field in ["address", "contact_number"]:
                fields.append(f"{field} = %s")
                values.append(value)
            elif isinstance(value, datetime):
                fields.append(f"{field} = %s")
                values.append(value.strftime('%Y-%m-%d %H:%M:%S'))
            else:
                fields.append(f"{field} = %s")
                values.append(value)

        if not fields:
            raise HTTPException(status_code=400, detail="No fields provided")

        values.append(email)
        set_clause = ", ".join(fields)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET {set_clause} WHERE email = %s", tuple(values))
        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "User profile updated successfully"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
