from sqlalchemy import Column, Integer, String, LargeBinary, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email_encrypted = Column(LargeBinary, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="viewer")

class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, nullable=False, default="default")
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, nullable=False)
    inputs_json = Column(Text)
    v_score = Column(Float, nullable=False)
    mc_json = Column(Text)
    diagnosis_json = Column(Text)
    audit_hash = Column(String)
