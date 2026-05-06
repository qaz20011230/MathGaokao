import os
import hashlib
import uuid
from typing import Optional
from fastapi import UploadFile

from app.config import settings


def get_document_dir() -> str:
    return settings.documents_path


def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower().lstrip(".")


def compute_md5(file_path: str) -> str:
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5.update(chunk)
    return md5.hexdigest()


def generate_filename(original_name: str, year: int, doc_type: str, province: Optional[str] = None) -> str:
    ext = get_file_extension(original_name)
    if not ext:
        ext = "pdf"
    parts = [str(year)]
    if province:
        parts.append(province)
    parts.append(doc_type)
    parts.append(uuid.uuid4().hex[:8])
    return f"{'—'.join(parts)}.{ext}"


async def save_upload(file: UploadFile, year: int, doc_type: str, province: Optional[str] = None) -> tuple[str, str, int]:
    doc_dir = get_document_dir()
    os.makedirs(doc_dir, exist_ok=True)

    period = "pre_1952" if year < 1952 else ("1952_1965" if year <= 1965 else "1977_now")
    period_dir = os.path.join(doc_dir, period)
    os.makedirs(period_dir, exist_ok=True)

    filename = generate_filename(file.filename or "document.pdf", year, doc_type, province)
    filepath = os.path.join(period_dir, filename)

    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)

    file_size = len(content)
    md5 = compute_md5(filepath)

    return filename, md5, file_size
