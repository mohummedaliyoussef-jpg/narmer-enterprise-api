from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, admin, analyst, viewer, assess
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ASAAS Insight Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(analyst.router)
app.include_router(viewer.router)

@app.get("/")
def root():
    return {"message": "ASAAS Insight Platform API"}

app.include_router(assess.router)
