from fastapi import APIRouter, Depends
from app.auth import require_role, get_current_user

router = APIRouter(prefix="/analyst", tags=["المحلل"])

@router.get("/reports")
def get_reports(current_user = Depends(require_role("analyst", "admin"))):
    return {"message": "تقارير المحللين"}
