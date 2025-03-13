from pydantic import BaseModel
from datetime import datetime
import uuid


class AlertRuleBase(BaseModel):
    server_id: uuid.UUID
    metric: str
    condition: str
    threshold: float
    duration: str
    notification_method: str


class AlertRuleCreate(AlertRuleBase):
    pass


class AlertRuleOut(AlertRuleBase):
    rule_id: int

    class Config:
        orm_mode = True