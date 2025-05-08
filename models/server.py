from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from datetime import datetime
import uuid
from sqlalchemy.orm import relationship


class Server(Base):
    __tablename__ = "servers"

    server_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hostname = Column(String, nullable=False)
    ip_address = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    owner     = relationship("User",      back_populates="servers")
    metrics   = relationship("Metric",    back_populates="server",
                             cascade="all, delete-orphan", passive_deletes=True)
    alerts    = relationship("Alert",     back_populates="server",
                             cascade="all, delete-orphan", passive_deletes=True)
    rules     = relationship("AlertRule", back_populates="server",
                             cascade="all, delete-orphan", passive_deletes=True)
    api_keys = relationship(
        "APIKey",
        back_populates="server_rel",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
