from celery import Celery
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import DATABASE_URL
from models.metric import Metric
from models.alert_rules import AlertRule
from models.alert import Alert
from datetime import datetime, timedelta

# Define Celery
celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Database Connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@celery.task
def check_alerts():
    """Check all active alert rules and create alerts if conditions are met."""
    db = SessionLocal()

    try:
        # Get all active alert rules
        alert_rules = db.query(AlertRule).all()

        for rule in alert_rules:
            # Fetch latest metrics for the server
            latest_metric = (
                db.query(Metric)
                .filter(Metric.server_id == rule.server_id)
                .order_by(Metric.timestamp.desc())
                .first()
            )

            if not latest_metric:
                continue  # No metrics yet

            # Check condition (e.g., CPU > threshold)
            metric_value = getattr(latest_metric, rule.metric)
            condition_met = eval(f"{metric_value} {rule.condition} {rule.threshold}")

            # Check if alert already exists
            active_alert = (
                db.query(Alert)
                .filter(Alert.server_id == rule.server_id, Alert.rule_id == rule.rule_id, Alert.status == "Triggered")
                .first()
            )

            if condition_met and not active_alert:
                # Create new alert
                new_alert = Alert(
                    server_id=rule.server_id,
                    rule_id=rule.rule_id,
                    triggered_at=datetime.utcnow(),
                    status="Triggered"
                )
                db.add(new_alert)
                print(f"Alert Triggered for {rule.metric} on Server {rule.server_id}")

            elif not condition_met and active_alert:
                # Resolve alert if condition is normal again
                active_alert.status = "Resolved"
                print(f"Alert Resolved for {rule.metric} on Server {rule.server_id}")

        db.commit()

    except Exception as e:
        print(f"Error checking alerts: {e}")
    finally:
        db.close()

