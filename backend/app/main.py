from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.documents import router as documents_router
from app.api.admin import router as admin_router
from app.database import engine, Base
from app.config import settings
from app.models.document import Document, Admin

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="mathgaokao.top API",
    description="高考数学试题档案馆 API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router)
app.include_router(admin_router)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "mathgaokao.top"}
