# file: app/schemas.py

from datetime import timedelta, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, SecretStr, Field
from fastapi import File, Form, UploadFile

from typing import List, Tuple


class BaseUser(BaseModel):
    username: EmailStr
    
    class Config:
        from_attributes = True



class CreateUser(BaseUser):
    first_name: str
    last_name: str
    password: str
    country: Optional[str] = None
    
    
class CreateAdmin(BaseUser):
    first_name: str
    last_name: str
    password: str 
    country: Optional[str] = None

    role: str = "admin"  
    is_active: bool = True  
    has_access_v1: bool = True  


class UserInfo(BaseUser):
    first_name: str
    last_name: str
    role: str
    country: Optional[str] = None

    
    
class ReadUser(UserInfo):
    id: int
    is_active: bool
    has_access_v1: bool



    
class ChangeUserAccessRights(BaseModel):
    is_active: bool
    has_access_v1: bool
    

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=4)




    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str
    user_id: int
    role: str
    has_access_v1: bool
    expires_delta: timedelta


class PredictionInput(BaseModel):
    audio_file: bytes = File(...)

    @classmethod
    def as_form(cls, audio_file: bytes = File(...)):
        return cls(audio_file=audio_file)
    
    
class SegmentPrediction(BaseModel):
    segment_start: float
    segment_end: float
    category: str
    probability: float


class Prediction(BaseModel):
    category: str
    probability: float

class PredictionOutput(BaseModel):
    predictions: List[Prediction]


class ServiceCallCreate(BaseModel):
    service_version: str
    success: bool
    owner_id: int
    request_time: datetime
    completion_time: datetime
    duration: float
    
    class Config:
        from_attributes = True
        

class ServiceCallRead(ServiceCallCreate):
    id: int


