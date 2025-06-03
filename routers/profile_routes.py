from fastapi import APIRouter, HTTPException, Depends
from jose import jwt, JWTError
from db import get_connection
from schemas import UpdateUserProfile
from auth import SECRET_KEY, ALGORITHM
from utils.token import oauth2_scheme
from pydantic import BaseModel
import json

router = APIRouter(prefix="/profile", tags=["User Profile"])

from schemas import UserAdmin, UserPatient

@router.get("/", response_model=UserAdmin | UserPatient)
def get_user_profile(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        role = payload.get("role")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if role == "admin":
            return UserAdmin(**user)

        for key in ["symptoms", "previous_treatments"]:
            if user.get(key):
                try:
                    user[key] = json.loads(user[key])
                except:
                    user[key] = []

        return UserPatient(**user)

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")



@router.put("/")
def update_profile(data: UpdateUserProfile, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        fields = []
        values = []

        for field, value in data.dict(exclude_unset=True).items():
            if field in ["symptoms", "previous_treatments"] and value is not None:
                fields.append(f"{field} = %s")
                values.append(json.dumps(value))
            elif value is not None:
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

        return {"message": "User profile updated successfully"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    finally:
        cursor.close()
        conn.close()


class AvatarUpload(BaseModel):
    avatar_url: str

@router.post("/avatar")
def upload_avatar(payload: AvatarUpload, token: str = Depends(oauth2_scheme)):
    try:
        payload_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload_data.get("sub")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET avatar_url = %s WHERE email = %s", (payload.avatar_url, email))
        conn.commit()

        return {"message": "Avatar uploaded successfully"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    finally:
        cursor.close()
        conn.close()
