from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.alert_rules import AlertRule
from schemas.alert_rules import AlertRuleCreate, AlertRuleOut
import uuid


router = APIRouter(prefix="/alert-rules", tags=["Alert Rules"])


@router.post("/", response_model=AlertRuleOut, status_code=status.HTTP_201_CREATED)
def create_alert_rule(rule_data: AlertRuleCreate, db: Session = Depends(get_db)):
    new_rule = AlertRule(**rule_data.dict())
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return new_rule


@router.get("/server/{server_id}", response_model=list[AlertRuleOut])
def list_alert_rules_for_server(server_id: uuid.UUID, db: Session = Depends(get_db)):
    return db.query(AlertRule).filter_by(server_id=server_id).all()


@router.get("/{rule_id}", response_model=AlertRuleOut)
def get_alert_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(AlertRule).filter_by(rule_id=rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")
    return rule


@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(AlertRule).filter_by(rule_id=rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")
    db.delete(rule)
    db.commit()
    return
