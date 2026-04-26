import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./asaas_insight.db")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
