from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from database import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(UUID(as_uuid=True), ForeignKey("servers.server_id", ondelete="CASCADE"), nullable=False)
    rule_id = Column(Integer, ForeignKey("alert_rules.rule_id", ondelete="CASCADE"), nullable=False)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False, default="Triggered")  # "Triggered" or "Resolved"


    server        = relationship("Server",     back_populates="alerts")
    rule          = relationship("AlertRule",  back_populates="alerts")
    notifications = relationship(
        "Notification",
        back_populates="alert",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
