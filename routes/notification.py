from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.notification import Notification
from schemas.notification import NotificationCreate, NotificationOut
from datetime import datetime
from routes.auth import get_current_user
from models.user import User

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/", response_model=NotificationOut, status_code=status.HTTP_201_CREATED)
def create_notification(notification_data: NotificationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_notification = Notification(
        alert_id=notification_data.alert_id,
        user_id=notification_data.user_id,
        method=notification_data.method,
        sent_at=datetime.utcnow()
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification

@router.get("/{user_id}", response_model=list[NotificationOut])
def list_notifications_for_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    notifications = db.query(Notification).filter_by(user_id=user_id).all()
    return notifications
