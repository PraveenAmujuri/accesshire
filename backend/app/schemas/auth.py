from typing import Optional
from pydantic import BaseModel, EmailStr

class AccessibilityPreferences(BaseModel):
    high_contrast: bool = False
    font_size: str = "medium"
    voice_mode_enabled: bool = False
    speech_rate: float = 1.0
    simplified_language: bool = False
    extended_response_time: bool = True

class UserRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    accessibility_preferences: Optional[AccessibilityPreferences] = None

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    name: str
    email: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    accessibility_preferences: AccessibilityPreferences
