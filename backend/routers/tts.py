from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from database import get_db
from models import Speech, User
from schemas import SpeechResponse, TTSRequest, Voice
from services.tts_service import VOICES, generate_audio
from utils.security import get_current_user

router = APIRouter(prefix="/api", tags=["speech"])
limiter = Limiter(key_func=get_remote_address)

def serialize_speech(speech: Speech) -> SpeechResponse:
    return SpeechResponse(id=speech.id, text=speech.text, language=speech.language, voice=speech.voice, speed=speech.speed, pitch=speech.pitch, volume=speech.volume, audio_url=speech.audio_path, created_at=speech.created_at)

@router.get("/voices", response_model=list[Voice])
def voices():
    return VOICES

@router.post("/parse-file")
async def parse_file(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".txt", ".pdf", ".docx"}:
        raise HTTPException(status_code=400, detail="Only TXT, PDF, and DOCX files are supported")
    content = await file.read()
    try:
        if suffix == ".txt":
            text = content.decode("utf-8-sig")
        elif suffix == ".pdf":
            from io import BytesIO
            from pypdf import PdfReader
            text = "\n".join(page.extract_text() or "" for page in PdfReader(BytesIO(content)).pages)
        else:
            from io import BytesIO
            from docx import Document
            text = "\n".join(paragraph.text for paragraph in Document(BytesIO(content)).paragraphs)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Could not extract text from this file") from exc
    return {"text": text[:5000]}

@router.post("/tts", response_model=SpeechResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def create_tts(request: Request, payload: TTSRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        _, audio_url = generate_audio(payload.text, payload.language, payload.speed, payload.pitch, payload.volume)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Audio generation failed. Please try again.") from exc
    speech = Speech(user_id=user.id, text=payload.text, language=payload.language, voice=payload.voice, speed=payload.speed, pitch=payload.pitch, volume=payload.volume, audio_path=audio_url)
    db.add(speech)
    db.commit()
    db.refresh(speech)
    return serialize_speech(speech)

@router.get("/history", response_model=list[SpeechResponse])
def history(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return [serialize_speech(item) for item in db.query(Speech).filter(Speech.user_id == user.id).order_by(Speech.created_at.desc()).limit(50).all()]
