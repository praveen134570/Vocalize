from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    speeches = relationship("Speech", back_populates="owner", cascade="all, delete-orphan")

class Speech(Base):
    __tablename__ = "speeches"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    text = Column(Text, nullable=False)
    language = Column(String(10), nullable=False)
    voice = Column(String(80), nullable=False, default="Standard")
    speed = Column(Float, nullable=False, default=1.0)
    pitch = Column(Float, nullable=False, default=1.0)
    volume = Column(Float, nullable=False, default=1.0)
    audio_path = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    owner = relationship("User", back_populates="speeches")
