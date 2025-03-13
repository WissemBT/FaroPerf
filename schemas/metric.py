from pydantic import BaseModel
from datetime import datetime
import uuid


class MetricBase(BaseModel):
    server_id: uuid.UUID
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_in: float
    network_out: float


class MetricCreate(MetricBase):
    pass


class MetricOut(MetricBase):
    metric_id: str

    class Config:
        orm_mode = True