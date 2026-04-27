from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text
from app import models
from app.database import get_db, get_encryption_key
from app.auth import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["المصادقة"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    username: str,
    password: str,
    role: str = "viewer",
    email: str = "user@insight.sa",
    db: Session = Depends(get_db)
):
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="اسم المستخدم موجود مسبقاً")

    hashed_pw = get_password_hash(password)

    sql = text("""
        INSERT INTO users (username, email_encrypted, hashed_password, role)
        VALUES (:username, pgp_sym_encrypt(:email, :key), :hashed_pw, :role)
    """)
    db.execute(sql, {
        "username": username,
        "email": email,
        "key": get_encryption_key(),
        "hashed_pw": hashed_pw,
        "role": role
    })
    db.commit()
    return {"message": f"تم إنشاء المستخدم {username} بدور {role}"}

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    sql = text("""
        SELECT id, username, pgp_sym_decrypt(email_encrypted, :key) AS email, hashed_password, role
        FROM users WHERE username = :username
    """)
    result = db.execute(sql, {
        "username": form_data.username,
        "key": get_encryption_key()
    }).first()

    if not result or not verify_password(form_data.password, result.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="بيانات دخول خاطئة"
        )

    access_token = create_access_token(data={"sub": result.username, "role": result.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh")
def refresh_token(current_user: models.User = Depends(get_current_user)):
    access_token = create_access_token(data={"sub": current_user.username, "role": current_user.role})
    return {"access_token": access_token, "token_type": "bearer"}
