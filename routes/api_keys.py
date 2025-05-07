import secrets
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.server import Server
from models.api_key import APIKey
from dependencies.api_key_auth import hash_key
from routes.auth import get_current_user
from models.user import User


router = APIRouter(
    prefix="/servers/{server_id}/keys",
    tags=["API Keys"],
)


def _owned_server(server_id: UUID, user_id: int, db: Session) -> Server:
    srv = (
        db.query(Server)
        .filter_by(server_id=server_id, user_id=user_id)
        .first()
    )
    if not srv:
        raise HTTPException(404, "Server not found or not owned by you")
    return srv


@router.post("/", status_code=status.HTTP_201_CREATED)
def generate_api_key(
    server_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _owned_server(server_id, current_user.user_id, db)

    raw_key = secrets.token_urlsafe(32)
    db.add(APIKey(key_hash=hash_key(raw_key), server=server_id))
    db.commit()
    return {"api_key": raw_key}  # show only once


@router.get("/", response_model=list[str])
def list_api_keys(
    server_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _owned_server(server_id, current_user.user_id, db)
    return [
        row.key_hash[:8] + "…"  # show shortened hash
        for row in db.query(APIKey)
        .filter_by(server=server_id, is_active=True)
        .all()
    ]


@router.delete("/{key_hash}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_api_key(
    server_id: UUID,
    key_hash: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _owned_server(server_id, current_user.user_id, db)
    row = (
        db.query(APIKey)
        .filter_by(server=server_id, key_hash=key_hash, is_active=True)
        .first()
    )
    if not row:
        raise HTTPException(404, "Key not found")
    row.is_active = False
    db.commit()
