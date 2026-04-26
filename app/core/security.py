from datetime import datetime, timedelta
from typing import Optional
import os
import hashlib
import secrets
from dotenv import load_dotenv
from jose import JWTError, jwt
from app.schemas import TokenData

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    parts = hashed_password.split("$")
    if len(parts) != 3:
        return False
    salt, key = parts[1], parts[2]
    new_key = hashlib.sha256(f"{salt}{plain_password}".encode()).hexdigest()
    return secrets.compare_digest(key, new_key)

def get_password_hash(password):
    salt = secrets.token_hex(16)
    key = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"sha256${salt}${key}"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            return None
        return TokenData(username=username, role=role)
    except JWTError:
        return None