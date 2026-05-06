from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class DocumentBase(BaseModel):
    title: str = Field(..., max_length=500, description="文档标题")
    year: int = Field(..., ge=1905, le=2025, description="年份")
    period: str = Field(..., description="时期: pre_1952, 1952_1965, 1977_now")
    doc_type: str = Field(..., description="类型: exam_paper, answer_sheet, answer_key, other")
    province: Optional[str] = Field(None, max_length=50, description="省份或高校名称")
    exam_category: Optional[str] = Field(None, max_length=50, description="理科/文科/新高考")
    description: Optional[str] = None
    source: Optional[str] = Field(None, max_length=200)
    year_title: Optional[str] = Field(None, max_length=100)
    is_published: int = Field(1, ge=0, le=1)


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=500)
    year: Optional[int] = Field(None, ge=1905, le=2025)
    period: Optional[str] = None
    doc_type: Optional[str] = None
    province: Optional[str] = Field(None, max_length=50)
    exam_category: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    source: Optional[str] = Field(None, max_length=200)
    year_title: Optional[str] = Field(None, max_length=100)
    is_published: Optional[int] = Field(None, ge=0, le=1)


class DocumentOut(DocumentBase):
    id: int
    file_path: str
    file_format: str
    file_size: int
    file_md5: Optional[str] = None
    page_count: Optional[int] = None
    download_count: int
    view_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DocumentListItem(BaseModel):
    id: int
    title: str
    year: int
    period: str
    doc_type: str
    province: Optional[str] = None
    exam_category: Optional[str] = None
    file_format: str
    page_count: Optional[int] = None
    file_size: int
    view_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class DocumentListOut(BaseModel):
    total: int
    items: list[DocumentListItem]
    page: int
    page_size: int


class YearStat(BaseModel):
    year: int
    count: int


class ProvinceStat(BaseModel):
    province: str
    count: int


class StatsOut(BaseModel):
    total_documents: int
    total_size_bytes: int
    years_covered: list[int]
    periods: dict[str, int]
    doc_types: dict[str, int]


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
