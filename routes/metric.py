from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.metric import Metric
from schemas.metric import MetricCreate, MetricOut
import uuid
from datetime import datetime
from routes.auth import get_current_user
from models.user import User
from models.server import Server


router = APIRouter(prefix="/metrics", tags=["Metrics"])


@router.post("/", response_model=MetricOut, status_code=status.HTTP_201_CREATED)
def create_metric(
    metric_data: MetricCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    server = db.query(Server).filter_by(server_id=metric_data.server_id, user_id=current_user.user_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found or not owned by you")
    new_metric = Metric(
        metric_id=str(uuid.uuid4()),
        server_id=metric_data.server_id,
        timestamp=metric_data.timestamp or datetime.utcnow(),
        cpu_usage=metric_data.cpu_usage,
        memory_usage=metric_data.memory_usage,
        disk_usage=metric_data.disk_usage,
        network_in=metric_data.network_in,
        network_out=metric_data.network_out,
    )
    db.add(new_metric); db.commit(); db.refresh(new_metric)
    return new_metric


@router.get("/{server_id}", response_model=list[MetricOut])
def list_metrics_for_server(
    server_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    if not db.query(Server).filter_by(server_id=server_id, user_id=current_user.user_id).first():
        raise HTTPException(status_code=404, detail="Server not found or not owned by you")
    return db.query(Metric).filter_by(server_id=server_id).all()