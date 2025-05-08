from sqlalchemy import Column, Integer, String, ForeignKey, Float
from database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship


class AlertRule(Base):
    __tablename__ = "alert_rules"

    rule_id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(UUID(as_uuid=True), ForeignKey("servers.server_id", ondelete="CASCADE"), nullable=False)
    metric = Column(String, nullable=False)
    condition = Column(String, nullable=False)
    threshold = Column(Float, nullable=False)
    duration = Column(String, nullable=False)
    notification_method = Column(String, nullable=False)

    server = relationship("Server", back_populates="rules")
    alerts = relationship(
        "Alert",
        back_populates="rule",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


