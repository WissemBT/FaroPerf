from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    alert_id = Column(
        Integer,
        ForeignKey("alerts.alert_id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    method = Column(String, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)

    alert = relationship("Alert", back_populates="notifications")
    user  = relationship("User",  back_populates="notifications")
