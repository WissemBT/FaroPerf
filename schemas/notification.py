from pydantic import BaseModel
from datetime import datetime

class NotificationBase(BaseModel):
    alert_id: int
    user_id: int
    method: str

class NotificationCreate(NotificationBase):
    pass

class NotificationOut(NotificationBase):
    notification_id: int
    sent_at: datetime

    class Config:
        orm_mode = True
