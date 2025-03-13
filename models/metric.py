from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from database import Base

from datetime  import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Metric(Base):
    __tablename__ = "metrics"

    metric_id = Column(String, primary_key=True)
    server_id = Column(UUID(as_uuid=True), ForeignKey("servers.server_id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    cpu_usage = Column(Float, nullable=False)
    memory_usage = Column(Float, nullable=False)
    disk_usage = Column(Float, nullable=False)
    network_in = Column(Float, nullable=False)
    network_out = Column(Float, nullable=False)
