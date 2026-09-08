from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Voice(BaseModel):
    language: str
    name: str
    code: str

class TTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    language: str = Field(default="en", pattern=r"^(en|hi|es|fr|de)$")
    voice: str = Field(default="Standard", max_length=80)
    speed: float = Field(default=1.0, ge=0.5, le=2.0)
    pitch: float = Field(default=1.0, ge=0.5, le=2.0)
    volume: float = Field(default=1.0, ge=0.0, le=1.0)

    @field_validator("text")
    @classmethod
    def text_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Text cannot be empty")
        return value

class SpeechResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    text: str
    language: str
    voice: str
    speed: float
    pitch: float
    volume: float
    audio_url: str
    created_at: datetime
