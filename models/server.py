from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from datetime import datetime
import uuid


class Server(Base):
    __tablename__ = "servers"

    server_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hostname = Column(String, nullable=False)
    ip_address = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
