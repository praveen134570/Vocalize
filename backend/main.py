import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from database import Base, engine
from routers import auth, tts

if os.getenv("AUTO_CREATE_TABLES", "false").lower() == "true":
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vocalize TTS API", version="1.0.0")
app.state.limiter = tts.limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
origins = [origin.strip().rstrip("/") for origin in os.getenv("FRONTEND_URL", "http://localhost:5173").split(",") if origin.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["Authorization", "Content-Type"])
app.include_router(auth.router)
app.include_router(tts.router)

@app.get("/api/health")
def health():
    return {"status": "ok"}
