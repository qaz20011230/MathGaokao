from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.document import DocumentListOut, DocumentListItem, DocumentOut, StatsOut, YearStat, ProvinceStat
from app.services import document as doc_service

router = APIRouter(prefix="/api", tags=["public"])


@router.get("/stats", response_model=StatsOut)
def get_stats(db: Session = Depends(get_db)):
    return doc_service.get_stats(db)


@router.get("/years", response_model=list[YearStat])
def get_years(db: Session = Depends(get_db)):
    return doc_service.get_years(db)


@router.get("/provinces", response_model=list[ProvinceStat])
def get_provinces(db: Session = Depends(get_db)):
    return doc_service.get_provinces(db)


@router.get("/documents", response_model=DocumentListOut)
def list_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    year: Optional[int] = Query(None),
    period: Optional[str] = Query(None),
    doc_type: Optional[str] = Query(None),
    province: Optional[str] = Query(None),
    exam_category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    items, total = doc_service.get_documents(
        db, page=page, page_size=page_size,
        year=year, period=period, doc_type=doc_type,
        province=province, exam_category=exam_category,
        search=search, published_only=True,
    )
    doc_items = [DocumentListItem.model_validate(d) for d in items]
    return DocumentListOut(total=total, items=doc_items, page=page, page_size=page_size)


@router.get("/documents/{doc_id}", response_model=DocumentOut)
def get_document(doc_id: int, db: Session = Depends(get_db)):
    doc = doc_service.get_document(db, doc_id)
    if not doc or not doc.is_published:
        raise HTTPException(status_code=404, detail="文档不存在")
    doc_service.increment_view(db, doc_id)
    return DocumentOut.model_validate(doc)


@router.get("/documents/{doc_id}/view")
def view_document(doc_id: int, db: Session = Depends(get_db)):
    doc = doc_service.get_document(db, doc_id)
    if not doc or not doc.is_published:
        raise HTTPException(status_code=404, detail="文档不存在")

    from fastapi.responses import FileResponse
    import os
    from app.config import settings

    file_path = os.path.join(settings.documents_path, doc.file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")

    doc_service.increment_view(db, doc_id)

    return FileResponse(
        file_path,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "inline",
            "X-Robots-Tag": "noindex",
        },
    )


@router.get("/documents/{doc_id}/viewer")
def viewer_html(doc_id: int, db: Session = Depends(get_db)):
    doc = doc_service.get_document(db, doc_id)
    if not doc or not doc.is_published:
        raise HTTPException(status_code=404, detail="文档不存在")

    from fastapi.responses import HTMLResponse
    import os
    from app.config import settings

    viewer_dir = os.path.join(settings.documents_path, os.path.dirname(doc.file_path), "html_viewer")
    viewer_path = os.path.join(viewer_dir, "viewer.html")

    if not os.path.exists(viewer_path):
        return RedirectResponse(url=f"/api/documents/{doc_id}/view")

    doc_service.increment_view(db, doc_id)

    with open(viewer_path, "r", encoding="utf-8") as f:
        html = f.read()

    return HTMLResponse(content=html)


@router.get("/documents/{doc_id}/pages/{filename:path}")
def serve_page_image(doc_id: int, filename: str, db: Session = Depends(get_db)):
    doc = doc_service.get_document(db, doc_id)
    if not doc or not doc.is_published:
        raise HTTPException(status_code=404, detail="文档不存在")

    from fastapi.responses import FileResponse
    import os
    from app.config import settings

    viewer_dir = os.path.join(settings.documents_path, os.path.dirname(doc.file_path), "html_viewer")
    file_path = os.path.join(viewer_dir, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")

    return FileResponse(file_path, media_type="image/png")
