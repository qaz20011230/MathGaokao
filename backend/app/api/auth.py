from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from app.config import settings
from app.database import get_db

security = HTTPBearer(auto_error=False)


def create_admin_token() -> str:
    payload = {
        "sub": "admin",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes),
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def verify_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload.get("type") == "access"
    except JWTError:
        return False


def get_current_admin(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> bool:
    if not credentials:
        return False
    return verify_token(credentials.credentials)


def require_admin(is_admin: bool = Depends(get_current_admin)):
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="需要管理员权限")
    return True
