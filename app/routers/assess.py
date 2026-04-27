from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user, get_current_tenant
from app.models import Assessment, User
from pydantic import BaseModel
import json

router = APIRouter(prefix="/api/assess", tags=["التقييم"])

class AssessmentCreate(BaseModel):
    inputs: dict
    v_score: float
    mc_data: dict | None = None
    diagnosis: dict | None = None
    audit_hash: str | None = None

@router.post("/")
def create_assessment(
    data: AssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant)
):
    assessment = Assessment(
        tenant_id=tenant_id,
        user_id=current_user.username,
        inputs_json=json.dumps(data.inputs),
        v_score=data.v_score,
        mc_json=json.dumps(data.mc_data) if data.mc_data else None,
        diagnosis_json=json.dumps(data.diagnosis) if data.diagnosis else None,
        audit_hash=data.audit_hash
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return {"id": assessment.id, "tenant": tenant_id}

@router.get("/")
def list_assessments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant)
):
    assessments = db.query(Assessment).filter(
        Assessment.tenant_id == tenant_id
    ).order_by(Assessment.created_at.desc()).limit(50).all()
    
    return [
        {
            "id": a.id,
            "tenant": a.tenant_id,
            "user": a.user_id,
            "inputs": json.loads(a.inputs_json) if a.inputs_json else None,
            "v_score": a.v_score,
            "created_at": a.created_at.isoformat() if a.created_at else None
        }
        for a in assessments
    ]
