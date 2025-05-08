import os
import hashlib
from datetime import datetime
from uuid import UUID

from fastapi import Header, HTTPException, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from models.api_key import APIKey

from dotenv import load_dotenv

load_dotenv()

PEPPER = os.getenv("API_KEY_PEPPER")


def hash_key(raw_key: str) -> str:
    return hashlib.sha256((raw_key + PEPPER).encode()).hexdigest()


def verify_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    db: Session = Depends(get_db),
) -> UUID:
    """
    Returns the server_id bound to a valid, active key.
    Raises 401 if missing / invalid / revoked.
    """
    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-API-Key header required",
        )

    key_hash = hash_key(x_api_key)
    row = (
        db.query(APIKey)
        .filter_by(key_hash=key_hash, is_active=True)
        .first()
    )
    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or revoked API key",
        )

    row.last_used = datetime.utcnow()
    db.commit()
    return row.server
