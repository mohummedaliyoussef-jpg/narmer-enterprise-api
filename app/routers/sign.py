from fastapi import APIRouter
from pydantic import BaseModel
from app.hsm import SovereignHSM

router = APIRouter(prefix="/sign", tags=["التوقيع الرقمي"])
hsm = SovereignHSM()

class Document(BaseModel):
    title: str
    content: dict

@router.post("/document")
def sign_document(doc: Document):
    signature = hsm.sign(doc.model_dump_json())
    public_key_hex = hsm.public_key.public_bytes_raw().hex()
    return {
        "public_key": public_key_hex,
        "signature": signature,
        "signed_content": doc.dict()
    }
