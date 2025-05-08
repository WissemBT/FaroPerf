from uuid import uuid4, UUID
from datetime import datetime

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.api_key_auth import verify_api_key
from routes.auth import get_current_user
from schemas.metric import MetricAgentCreate, MetricOut
from models.metric import Metric
from models.server import Server
from models.user import User


router = APIRouter(prefix="/metrics", tags=["Metrics"])


@router.post(
    "/",
    response_model=MetricOut,
    status_code=status.HTTP_201_CREATED
)
def create_metric_agent(
    payload: MetricAgentCreate,
    server_id: UUID = Depends(verify_api_key),
    db: Session = Depends(get_db),
    ):
    new_metric = Metric(
        metric_id=str(uuid4()),
        server_id=server_id,
        timestamp=payload.timestamp or datetime.utcnow(),
        cpu_usage=payload.cpu_usage,
        memory_usage=payload.memory_usage,
        disk_usage=payload.disk_usage,
        network_in=payload.network_in,
        network_out=payload.network_out,
    )
    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)
    return new_metric


@router.get("/{server_id}", response_model=list[MetricOut])
def list_metrics_for_server(
    server_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):
    if not db.query(Server).filter_by(
        server_id=server_id, user_id=current_user.user_id
    ).first():
        raise HTTPException(status_code=404, detail="Server not found or not owned by you")

    return db.query(Metric).filter_by(server_id=server_id).all()
