from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class GenderEnum(str, Enum):
    M = "M"
    F = "F"

class RegisterSchema(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

class LoginSchema(BaseModel):
    email: str
    password: str

# class ScanUploadSchema(BaseModel):
#     image_url: str
#     oral_health_score: Optional[int] = None
#     ai_feedback: Optional[str] = None
#     detected_conditions: Optional[str] = None

class UpdateUserProfile(BaseModel):
    gender: Optional[GenderEnum] = None
    date_of_birth: Optional[datetime] = None
    under_physician_care: Optional[bool] = None
    chronic_conditions: Optional[bool] = None
    any_allergies: Optional[bool] = None
    under_medications: Optional[bool] = None
    pregnant_or_nursing: Optional[bool] = None
    symptoms: Optional[List[str]] = None
    previous_treatments: Optional[List[str]] = None
    diagnosed_gum_disease: Optional[bool] = None
    brushing_frequency: Optional[str] = None
    flossing: Optional[bool] = None
    tobacco_use: Optional[bool] = None
    sugary_diet: Optional[bool] = None
    teeth_grinding: Optional[bool] = None
    is_subscribed: Optional[bool] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None


class DoctorOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    short_bio: Optional[str]
    gender: Optional[str]
    specialty: Optional[str]
    languages: Optional[str]
    rating: Optional[float]
    profile_image: Optional[str]
    city: Optional[str]

    class Config:
        from_attributes = True

class StatusUpdate(BaseModel):
    status: str  # You can later restrict with Enum if needed

class UserBase(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: str

class UserAdmin(UserBase):
    pass

class UserPatient(UserBase):
    gender: Optional[GenderEnum] = None
    date_of_birth: Optional[datetime] = None
    avatar_url: Optional[str] = None
    under_physician_care: Optional[bool] = None
    chronic_conditions: Optional[bool] = None
    any_allergies: Optional[bool] = None
    under_medications: Optional[bool] = None
    pregnant_or_nursing: Optional[bool] = None
    symptoms: Optional[List[str]] = None
    previous_treatments: Optional[List[str]] = None
    diagnosed_gum_disease: Optional[bool] = None
    brushing_frequency: Optional[str] = None
    flossing: Optional[bool] = None
    tobacco_use: Optional[bool] = None
    sugary_diet: Optional[bool] = None
    teeth_grinding: Optional[bool] = None
    is_subscribed: Optional[bool] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None

