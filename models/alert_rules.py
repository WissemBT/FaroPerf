from sqlalchemy import Column, Integer, String, ForeignKey, Float
from database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class AlertRule(Base):
    __tablename__ = "alert_rules"

    rule_id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(UUID(as_uuid=True), ForeignKey("servers.server_id"), nullable=False)
    metric = Column(String, nullable=False)
    condition = Column(String, nullable=False)
    threshold = Column(Float, nullable=False)
    duration = Column(String, nullable=False)
    notification_method = Column(String, nullable=False)

