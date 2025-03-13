from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.metric import Metric
from schemas.metric import MetricCreate, MetricOut
import uuid
from datetime import datetime

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.post("/",response_model=MetricOut, status_code=status.HTTP_201_CREATED)
def create_metric(metric_data: MetricCreate, db: Session= Depends(get_db)):
    new_metric = Metric(
        metric_id=str(uuid.uuid4()),
        server_id=metric_data.server_id,
        timestamp=metric_data.timestamp or datetime.utcnow(),
        cpu_usage=metric_data.cpu_usage,
        memory_usage=metric_data.memory_usage,
        disk_usage=metric_data.disk_usage,
        network_in=metric_data.network_in,
        network_out=metric_data.network_out
    )

    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)
    return new_metric

@router.get("/{server_id}",response_model=list[MetricOut])
def get_metrics_for_server(server_id: uuid.UUID, db: Session = Depends(get_db)):
    metrics = db.query(Metric).filter_by(server_id=server_id).all()
    return metrics