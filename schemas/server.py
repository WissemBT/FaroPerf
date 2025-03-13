from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid


class ServerBase(BaseModel):
    hostname: str
    ip_address: str

class ServerCreate(ServerBase):
    pass

class ServerUpdate(BaseModel):
    hostname: Optional[str] = None
    ip_address: Optional[str] = None

class ServerOut(ServerBase):
    server_id: uuid.UUID
    created_at: datetime

    class Config:
        orm_mode = True
