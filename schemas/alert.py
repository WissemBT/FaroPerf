from pydantic import BaseModel
from datetime import datetime
import uuid


class AlertBase(BaseModel):
    server_id: uuid.UUID
    rule_id: int
    triggered_at: datetime = datetime.utcnow()
    status: str = "Triggered"  # or "Resolved"

class AlertCreate(AlertBase):
    pass

class AlertOut(AlertBase):
    alert_id: int

    class Config:
        orm_mode = True

