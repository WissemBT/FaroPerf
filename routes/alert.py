from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.alert import Alert
from schemas.alert import AlertCreate, AlertOut
from datetime import datetime
from routes.auth import get_current_user
from models.user import User
from models.server import Server

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.post("/", response_model=AlertOut, status_code=status.HTTP_201_CREATED)
def create_alert(
    alert_data: AlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    if not db.query(Server).filter_by(server_id=alert_data.server_id, user_id=current_user.user_id).first():
        raise HTTPException(status_code=404, detail="Server not found or not owned by you")
    new_alert = Alert(
        server_id=alert_data.server_id,
        rule_id=alert_data.rule_id,
        triggered_at=alert_data.triggered_at or datetime.utcnow(),
        status=alert_data.status,
    )
    db.add(new_alert); db.commit(); db.refresh(new_alert)
    return new_alert


@router.get("/{alert_id}", response_model=AlertOut)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    alert = db.query(Alert).join(Server, Alert.server_id == Server.server_id).\
        filter(Alert.alert_id == alert_id, Server.user_id == current_user.user_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.put("/{alert_id}", response_model=AlertOut)
def update_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    alert = db.query(Alert).join(Server, Alert.server_id == Server.server_id).\
        filter(Alert.alert_id == alert_id, Server.user_id == current_user.user_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.status = "Resolved"; db.commit(); db.refresh(alert)
    return alert


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    alert = db.query(Alert).join(Server, Alert.server_id == Server.server_id).\
        filter(Alert.alert_id == alert_id, Server.user_id == current_user.user_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(alert); db.commit()
