from datetime import datetime

from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database import Base
from sqlalchemy.orm import relationship

class APIKey(Base):
    __tablename__ = "api_keys"

    key_hash = Column(String, primary_key=True, index=True)
    server = Column(UUID(as_uuid=True), ForeignKey("servers.server_id", ondelete="CASCADE"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime)

    server_rel = relationship(
        "Server",
        back_populates="api_keys",
        foreign_keys=[server],
        passive_deletes=True,
    )