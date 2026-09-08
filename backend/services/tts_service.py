import io
import os
import uuid
from gtts import gTTS
from supabase import Client, create_client

LANGUAGES = {"en": "English", "hi": "Hindi", "es": "Spanish", "fr": "French", "de": "German"}
VOICES = [{"language": label, "name": "Standard", "code": code} for code, label in LANGUAGES.items()]
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "audio")


def get_storage_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("Supabase Storage is not configured")
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def generate_audio(text: str, language: str, speed: float = 1.0, pitch: float = 1.0, volume: float = 1.0) -> tuple[str, str]:
    # gTTS currently exposes language and slow mode; pitch/volume remain part of the provider-neutral contract.
    buffer = io.BytesIO()
    gTTS(text=text, lang=language, slow=speed < 0.78).write_to_fp(buffer)
    buffer.seek(0)
    path = f"{uuid.uuid4().hex}.mp3"
    get_storage_client().storage.from_(SUPABASE_BUCKET).upload(path, buffer.getvalue(), {"content-type": "audio/mpeg", "upsert": "false"})
    public_url = get_storage_client().storage.from_(SUPABASE_BUCKET).get_public_url(path)
    return path, public_url
