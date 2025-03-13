from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from database import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(UUID(as_uuid=True), ForeignKey("servers.server_id"), nullable=False)
    rule_id = Column(Integer, ForeignKey("alert_rules.rule_id"), nullable=False)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False, default="Triggered")  # "Triggered" or "Resolved"
