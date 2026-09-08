# Vocalize

Vocalize is a full-stack text-to-speech web application with a React/Vite frontend and FastAPI backend. It supports JWT authentication, speech generation through a swappable TTS service boundary, history, audio downloads, and TXT/PDF/DOCX imports.

## Stack

- React 18 + Vite + Tailwind CSS
- FastAPI + SQLAlchemy + Pydantic
- PostgreSQL in production, SQLite fallback for local development
- gTTS provider abstraction
- JWT authentication with bcrypt password hashing

## Local setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --port 8000
```

Set `DATABASE_URL` to a PostgreSQL URL for production. The default SQLite URL is convenient for local development. gTTS requires network access to generate audio.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_URL` if the backend is not running at `http://localhost:8000`.

## API overview

- `GET /api/health` — health check
- `GET /api/voices` — available language and voice options
- `POST /auth/register` and `POST /auth/login` — JWT authentication
- `POST /api/tts` — generate and save an MP3 (10 requests per minute per client)
- `GET /api/history` — authenticated speech history
- `POST /api/parse-file` — authenticated TXT/PDF/DOCX extraction
- `GET /api/audio/{filename}` — stream a generated MP3

## Production notes

Use a strong `SECRET_KEY`, PostgreSQL, HTTPS, and a managed or persistent audio storage policy. The included audio directory is intended for a local prototype; add object storage and lifecycle cleanup when deploying at scale.
