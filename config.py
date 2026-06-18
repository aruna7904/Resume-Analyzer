import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "data/resume_agent.db")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # Enforce 5 MB upload boundary