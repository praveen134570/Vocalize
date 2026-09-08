from fastapi import FastAPI

try:
    from main import app as application
except Exception as exc:
    print(f"Application startup warning: {exc}")
    application = None

app = application or FastAPI(title="Vocalize TTS API", version="1.0.0")

if application is None:
    @app.get("/api/health")
    def health():
        return {"status": "ok", "mode": "degraded"}

    @app.get("/api/voices")
    def voices():
        return [
            {"language": "English", "name": "Standard", "code": "en"},
            {"language": "Hindi", "name": "Standard", "code": "hi"},
            {"language": "Spanish", "name": "Standard", "code": "es"},
            {"language": "French", "name": "Standard", "code": "fr"},
            {"language": "German", "name": "Standard", "code": "de"},
        ]

__all__ = ["app"]

# Vercel deployment entrypoint.

# Native Vercel FastAPI settings are configured in the project dashboard.

# Redeploy after native Vercel command overrides were disabled.
