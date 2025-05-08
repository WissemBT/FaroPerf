"""
Periodic Celery task:
    • Evaluate alert-rules
    • Insert / resolve Alert rows
    • Insert Notification rows

Start:
    celery -A tasks.alerting worker --loglevel=info
    celery -A tasks.alerting beat   --loglevel=info

TODO: Temporary solution, should  be changed in the future
not best solution when scaling up
"""
from __future__ import annotations

import logging
import operator
import re
from datetime import datetime, timedelta
from uuid import UUID

from celery import Celery
from celery.schedules import crontab
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from database import DATABASE_URL
from models.metric import Metric
from models.server import Server
from models.alert_rules import AlertRule
from models.alert import Alert
from models.notification import Notification


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


celery = Celery(
    "alerting",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery.conf.beat_schedule = {
    "check-alert-rules-every-minute": {
        "task": "tasks.alerting.check_alerts",
        "schedule": crontab(minute="*"),
    }
}


_OPS = {">": operator.gt, "<": operator.lt, ">=": operator.ge,
        "<=": operator.le, "==": operator.eq}

_DUR_RE = re.compile(r"^(\d+)([smhd])$")

def _parse_seconds(expr: str) -> int:
    m = _DUR_RE.fullmatch(expr.strip())
    if not m:
        raise ValueError(f"Bad duration '{expr}'")
    value, unit = m.groups()
    value = int(value)
    return value * {"s": 1, "m": 60, "h": 3600, "d": 86_400}[unit]


_engine = create_engine(DATABASE_URL, pool_pre_ping=True)
_SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)


@celery.task(name="tasks.alerting.check_alerts")
def check_alerts() -> None:
    """Main loop executed every minute by Celery-beat."""
    now = datetime.utcnow()
    db: Session = _SessionLocal()

    logger.info("🔍  Running alert evaluation at %s", now.isoformat(timespec="seconds"))

    try:
        for rule in db.query(AlertRule).all():
            try:
                window = timedelta(seconds=_parse_seconds(rule.duration))
            except ValueError as e:
                logger.warning("Rule %s skipped (bad duration): %s", rule.rule_id, e)
                continue

            metric: Metric | None = (
                db.query(Metric)
                .filter(
                    Metric.server_id == rule.server_id,
                    Metric.timestamp >= now - window
                )
                .order_by(Metric.timestamp.desc())
                .first()
            )

            if not metric:
                logger.debug("Rule %s has no recent metric — skip", rule.rule_id)
                continue

            metric_val = getattr(metric, rule.metric)
            passed = _OPS[rule.condition](metric_val, rule.threshold)

            active: Alert | None = (
                db.query(Alert)
                .filter_by(server_id=rule.server_id,
                           rule_id=rule.rule_id,
                           status="Triggered")
                .first()
            )

            if passed and not active:
                new_alert = Alert(
                    server_id=rule.server_id,
                    rule_id=rule.rule_id,
                    triggered_at=now,
                    status="Triggered",
                )
                db.add(new_alert)
                db.flush()
                server = db.query(Server).filter_by(server_id=rule.server_id).first()
                db.add(Notification(
                    alert_id=new_alert.alert_id,
                    user_id=server.user_id if server else None,
                    method=rule.notification_method,
                    sent_at=now,
                ))

                logger.info(
                    "Alert TRIGGERED  rule=%s server=%s value=%s%s%s",
                    rule.rule_id, rule.server_id,
                    metric_val, rule.condition, rule.threshold,
                )

            elif not passed and active:
                active.status = "Resolved"
                logger.info(
                    "Alert RESOLVED   rule=%s server=%s back-to-normal (%s)",
                    rule.rule_id, rule.server_id, metric_val,
                )

        db.commit()

    except Exception:
        logger.exception("Fatal error in check_alerts loop — rolled back")
        db.rollback()
    finally:
        db.close()
