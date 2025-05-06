from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.notification import Notification
from schemas.notification import NotificationCreate, NotificationOut
from datetime import datetime
from routes.auth import get_current_user
from models.user import User
from models.server import Server
from models.alert import Alert


router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.post("/", response_model=NotificationOut, status_code=status.HTTP_201_CREATED)
def create_notification(
    notification_data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    alert = db.query(Alert).join(Server, Alert.server_id == Server.server_id).\
        filter(Alert.alert_id == notification_data.alert_id, Server.user_id == current_user.user_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found or not owned by you")
    new_notification = Notification(
        alert_id=notification_data.alert_id,
        user_id=current_user.user_id,
        method=notification_data.method,
        sent_at=datetime.utcnow(),
    )
    db.add(new_notification); db.commit(); db.refresh(new_notification)
    return new_notification


@router.get("/", response_model=list[NotificationOut])
def list_my_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return db.query(Notification).filter_by(user_id=current_user.user_id).all()
