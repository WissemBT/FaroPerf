from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.server import Server
from schemas.server import ServerCreate, ServerUpdate, ServerOut
from datetime import datetime
import uuid

router = APIRouter(prefix="/servers", tags=["Servers"])

@router.post("/", response_model=ServerOut, status_code=status.HTTP_201_CREATED)
def create_server(server_data: ServerCreate, db: Session = Depends(get_db)):
    existing_server = db.query(Server).filter_by(ip_address=server_data.ip_address).first()
    if existing_server:
        raise HTTPException(status_code=400, detail="IP address already in use!")

    new_server = Server(
        hostname=server_data.hostname,
        ip_address=server_data.ip_address,
    )

    db.add(new_server)
    db.commit()
    db.refresh(new_server)
    return new_server


@router.get("/", response_model=list[ServerOut])
def list_servers(db: Session=Depends(get_db)):
    return db.query(Server).all()


@router.get("/{server_id}", response_model=ServerOut)
def get_server(server_id: uuid.UUID, db: Session = Depends(get_db)):
    server = db.query(Server).filter_by(server_id=server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    return server

@router.put("/{server_id}", response_model=ServerOut)
def update_server(server_id: uuid.UUID, updates: ServerUpdate, db: Session = Depends(get_db)):
    server = db.query(Server).filter_by(server_id=server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    if updates.hostname is not None:
        server.hostname = updates.hostname
    if updates.ip_address is not None:
        existing_server = db.query(Server).filter_by(ip_address=updates.ip_address).first()
        if existing_server and existing_server.server_id != server_id:
            raise HTTPException(status_code=400, detail="IP address already in use!")

        server.ip_address = updates.ip_address

    db.commit()
    db.refresh(server)
    return server

@router.delete("/{server_id}", status_code=status.HTTP_204_NO_CONTENT)
def deleter_server(server_id: uuid.UUID, db: Session = Depends(get_db)):
    server = db.query(Server).filter_by(server_id=server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    db.delete(server)
    db.commit()
    return