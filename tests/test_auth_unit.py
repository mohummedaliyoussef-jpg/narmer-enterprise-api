import pytest
from datetime import timedelta
from app.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)
from jose import jwt

def test_hash_password():
    password = "mysecret"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True

def test_verify_wrong_password():
    password = "mysecret"
    hashed = get_password_hash(password)
    assert verify_password("wrongpass", hashed) is False

def test_create_access_token():
    data = {"sub": "admin", "role": "admin"}
    token = create_access_token(data=data)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get("sub") == "admin"
    assert payload.get("role") == "admin"
    assert "exp" in payload

def test_token_expiration():
    data = {"sub": "test"}
    token = create_access_token(data=data, expires_delta=timedelta(seconds=-1))
    with pytest.raises(Exception):
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
