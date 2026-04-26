from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models
from app.auth import get_db, get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["المصادقة"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    username: str,
    password: str,
    role: str = "viewer",
    email: str = "no-reply@insight.sa",
    db: Session = Depends(get_db)
):
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="اسم المستخدم موجود مسبقاً")
    hashed_pw = get_password_hash(password)
    new_user = models.User(username=username, email=email, hashed_password=hashed_pw, role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"تم إنشاء المستخدم {username} بدور {role}"}

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="بيانات دخول خاطئة"
        )
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh")
def refresh_token(current_user: models.User = Depends(get_current_user)):
    access_token = create_access_token(data={"sub": current_user.username, "role": current_user.role})
    return {"access_token": access_token, "token_type": "bearer"}