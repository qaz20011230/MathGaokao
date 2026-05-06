import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from app.database import get_db
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentOut, DocumentListOut, DocumentListItem, LoginRequest, TokenOut
from app.services import document as doc_service
from app.api.auth import create_admin_token, require_admin
from app.utils.file_handler import save_upload
from app.config import settings
from passlib.hash import bcrypt

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/login", response_model=TokenOut)
def login(data: LoginRequest):
    if data.username != settings.admin_username or not bcrypt.verify(data.password, bcrypt.hash(settings.admin_password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = create_admin_token()
    return TokenOut(access_token=token)


@router.post("/documents", response_model=DocumentOut, dependencies=[Depends(require_admin)])
async def create_document(
    title: str = Form(...),
    year: int = Form(...),
    period: str = Form(...),
    doc_type: str = Form(...),
    province: str = Form(None),
    exam_category: str = Form(None),
    description: str = Form(None),
    source: str = Form(None),
    year_title: str = Form(None),
    is_published: int = Form(1),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    filename, md5, size = await save_upload(file, year, doc_type, province)
    doc_data = DocumentCreate(
        title=title, year=year, period=period, doc_type=doc_type,
        province=province or None,
        exam_category=exam_category or None,
        description=description or None,
        source=source or None,
        year_title=year_title or None,
        is_published=is_published,
    )
    doc = doc_service.create_document(db, doc_data, filename, md5, size)
    return DocumentOut.model_validate(doc)


@router.put("/documents/{doc_id}", response_model=DocumentOut, dependencies=[Depends(require_admin)])
def update_document(doc_id: int, data: DocumentUpdate, db: Session = Depends(get_db)):
    doc = doc_service.update_document(db, doc_id, data)
    if not doc:
        raise HTTPException(status_code=404, detail="文档不存在")
    return DocumentOut.model_validate(doc)


@router.delete("/documents/{doc_id}", dependencies=[Depends(require_admin)])
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    success = doc_service.delete_document(db, doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="文档不存在")
    return {"detail": "删除成功"}


@router.get("/documents/{doc_id}/download", dependencies=[Depends(require_admin)])
def download_document(doc_id: int, db: Session = Depends(get_db)):
    doc = doc_service.get_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="文档不存在")
    file_path = os.path.join(settings.documents_path, doc.file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    return FileResponse(
        file_path,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={doc.title}.pdf"},
    )


@router.get("/documents", response_model=DocumentListOut, dependencies=[Depends(require_admin)])
def list_all_documents(
    page: int = 1,
    page_size: int = 50,
    db: Session = Depends(get_db),
):
    items, total = doc_service.get_documents(db, page=page, page_size=page_size, published_only=False)
    doc_items = [DocumentListItem.model_validate(d) for d in items]
    return DocumentListOut(total=total, items=doc_items, page=page, page_size=page_size)


@router.get("/auth/check")
def check_auth(is_admin: bool = Depends(require_admin)):
    return {"authenticated": True}
