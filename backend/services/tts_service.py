import os
import uuid
from pathlib import Path
from gtts import gTTS

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "./uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

LANGUAGES = {"en": "English", "hi": "Hindi", "es": "Spanish", "fr": "French", "de": "German"}
VOICES = [{"language": label, "name": "Standard", "code": code} for code, label in LANGUAGES.items()]

def generate_audio(text: str, language: str, speed: float = 1.0, pitch: float = 1.0, volume: float = 1.0) -> str:
    # gTTS exposes language and slow mode; the remaining controls are accepted for provider portability.
    filename = f"{uuid.uuid4().hex}.mp3"
    path = UPLOAD_DIR / filename
    gTTS(text=text, lang=language, slow=speed < 0.78).save(str(path))
    return filename
