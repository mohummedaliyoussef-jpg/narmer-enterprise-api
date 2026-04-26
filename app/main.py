from fastapi import FastAPI
from app.routers import auth, admin, analyst, viewer
from app.database import engine, Base

# إنشاء الجداول تلقائياً عند التشغيل (للتطوير فقط)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ASAAS Insight Platform", version="1.0.0")

# تضمين الراوترات (بدون prefix مكرر)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(analyst.router)
app.include_router(viewer.router)

@app.get("/")
def root():
    return {"message": "ASAAS Insight Platform is running"}

