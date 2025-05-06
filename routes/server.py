from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.server import Server
from schemas.server import ServerCreate, ServerUpdate, ServerOut
from datetime import datetime
import uuid
from routes.auth import get_current_user
from models.user import User


router = APIRouter(prefix="/servers", tags=["Servers"])


@router.post("/", response_model=ServerOut, status_code=status.HTTP_201_CREATED)
def create_server(
    server_data: ServerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if db.query(Server).filter_by(ip_address=server_data.ip_address, user_id=current_user.user_id).first():
        raise HTTPException(status_code=400, detail="IP address already in use!")

    new_server = Server(
        hostname=server_data.hostname,
        ip_address=server_data.ip_address,
        user_id=current_user.user_id,
    )
    db.add(new_server)
    db.commit()
    db.refresh(new_server)
    return new_server


@router.get("/", response_model=list[ServerOut])
def list_servers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return db.query(Server).filter_by(user_id=current_user.user_id).all()


@router.get("/{server_id}", response_model=ServerOut)
def get_server(
    server_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    server = db.query(Server).filter_by(server_id=server_id, user_id=current_user.user_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server


@router.put("/{server_id}", response_model=ServerOut)
def update_server(
    server_id: uuid.UUID,
    updates: ServerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    server = db.query(Server).filter_by(server_id=server_id, user_id=current_user.user_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    if updates.hostname is not None:
        server.hostname = updates.hostname
    if updates.ip_address is not None:
        if db.query(Server).filter(Server.ip_address == updates.ip_address, Server.user_id == current_user.user_id, Server.server_id != server_id).first():
            raise HTTPException(status_code=400, detail="IP address already in use!")
        server.ip_address = updates.ip_address
    db.commit(); db.refresh(server)
    return server


@router.delete("/{server_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_server(
    server_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    server = db.query(Server).filter_by(server_id=server_id, user_id=current_user.user_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    db.delete(server); db.commit()