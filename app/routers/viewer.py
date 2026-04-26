from fastapi import APIRouter, Depends
from app.auth import require_role, get_current_user

router = APIRouter(prefix="/viewer", tags=["المشاهد"])

@router.get("/public-data")
def public_data(current_user = Depends(require_role("viewer", "analyst", "admin"))):
    return {"message": "بيانات عامة"}
