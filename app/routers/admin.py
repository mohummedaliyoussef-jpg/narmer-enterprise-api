from fastapi import APIRouter, Depends
from app.auth import require_role, get_current_user

router = APIRouter(prefix="/admin", tags=["المدير"])

@router.get("/users")
def list_users(current_user = Depends(require_role("admin"))):
    return {"message": f"مرحباً بك في لوحة التحكم الإدارية، {current_user.username}"}
