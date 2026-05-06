import os
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.models.document import Document, Admin
from app.schemas.document import (
    DocumentCreate, DocumentUpdate, DocumentOut, DocumentListItem,
    YearStat, ProvinceStat, StatsOut
)
from app.config import settings


def get_document(db: Session, doc_id: int) -> Optional[Document]:
    return db.query(Document).filter(Document.id == doc_id).first()


def get_documents(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    year: Optional[int] = None,
    period: Optional[str] = None,
    doc_type: Optional[str] = None,
    province: Optional[str] = None,
    exam_category: Optional[str] = None,
    search: Optional[str] = None,
    published_only: bool = True,
) -> tuple[list[Document], int]:
    q = db.query(Document)

    if published_only:
        q = q.filter(Document.is_published == 1)

    if year:
        q = q.filter(Document.year == year)
    if period:
        q = q.filter(Document.period == period)
    if doc_type:
        q = q.filter(Document.doc_type == doc_type)
    if province:
        q = q.filter(Document.province == province)
    if exam_category:
        q = q.filter(Document.exam_category == exam_category)

    if search:
        q = q.filter(
            Document.title.contains(search) |
            Document.description.contains(search) |
            Document.province.contains(search)
        )

    total = q.count()
    items = q.order_by(Document.year.asc(), Document.title.asc()) \
        .offset((page - 1) * page_size) \
        .limit(page_size) \
        .all()

    return items, total


def create_document(db: Session, data: DocumentCreate, file_path: str, file_md5: str, file_size: int) -> Document:
    doc = Document(
        title=data.title,
        year=data.year,
        period=data.period,
        doc_type=data.doc_type,
        province=data.province,
        exam_category=data.exam_category,
        file_path=file_path,
        file_format="pdf",
        file_size=file_size,
        file_md5=file_md5,
        description=data.description,
        source=data.source,
        year_title=data.year_title,
        is_published=data.is_published,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def update_document(db: Session, doc_id: int, data: DocumentUpdate) -> Optional[Document]:
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(doc, key, value)
    db.commit()
    db.refresh(doc)
    return doc


def delete_document(db: Session, doc_id: int) -> bool:
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        return False
    file_full_path = os.path.join(settings.documents_path, doc.file_path)
    if os.path.exists(file_full_path):
        os.remove(file_full_path)
    db.delete(doc)
    db.commit()
    return True


def increment_view(db: Session, doc_id: int):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if doc:
        doc.view_count += 1
        db.commit()


def get_years(db: Session) -> list[YearStat]:
    results = db.query(Document.year, func.count(Document.id).label("count")) \
        .filter(Document.is_published == 1) \
        .group_by(Document.year) \
        .order_by(Document.year.asc()) \
        .all()
    return [YearStat(year=r[0], count=r[1]) for r in results]


def get_provinces(db: Session) -> list[ProvinceStat]:
    results = db.query(Document.province, func.count(Document.id).label("count")) \
        .filter(Document.is_published == 1, Document.province.isnot(None)) \
        .group_by(Document.province) \
        .order_by(func.count(Document.id).desc()) \
        .all()
    return [ProvinceStat(province=r[0], count=r[1]) for r in results]


def get_stats(db: Session) -> StatsOut:
    total = db.query(func.count(Document.id)).filter(Document.is_published == 1).scalar() or 0
    total_size = db.query(func.sum(Document.file_size)).filter(Document.is_published == 1).scalar() or 0

    years_raw = db.query(Document.year).filter(Document.is_published == 1).distinct().order_by(Document.year.asc()).all()
    years_list = [r[0] for r in years_raw]

    period_counts = db.query(Document.period, func.count(Document.id)) \
        .filter(Document.is_published == 1).group_by(Document.period).all()
    periods = {r[0]: r[1] for r in period_counts}

    type_counts = db.query(Document.doc_type, func.count(Document.id)) \
        .filter(Document.is_published == 1).group_by(Document.doc_type).all()
    doc_types = {r[0]: r[1] for r in type_counts}

    return StatsOut(
        total_documents=total,
        total_size_bytes=total_size,
        years_covered=years_list,
        periods=periods,
        doc_types=doc_types,
    )
