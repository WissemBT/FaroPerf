import psutil
import requests
import time
import uuid
from datetime import datetime


SERVER_ID = str(uuid.uuid4())
BACKEND_URL = "http://127.0.0.1:8000/metrics/"
INTERVAL = 20 # every 20 s

def collect_metrics():
    """Collect system metrics using psutil"""
    return {
        "server_id": SERVER_ID,
        "timestamp": datetime.utcnow().isoformat(),
        "cpu_usage": psutil.cpu_percent(interval=1),  # 1 sec average CPU usage
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "network_in": psutil.net_io_counters().bytes_recv / (1024 * 1024),  # Convert to MB
        "network_out": psutil.net_io_counters().bytes_sent / (1024 * 1024)  # Convert to MB
    }

def send_metrics():
    """Send collected metrics to the FastAPI backend."""
    while True:
        try:
            data = collect_metrics()
            response = requests.post(BACKEND_URL, json=data)

            if response.status_code == 201:
                print(f"[{datetime.utcnow()}] Metrics sent successfully")
            else:
                print(f"[{datetime.utcnow()}] Failed to send metrics: {response.text}")

        except Exception as e:
            print(f"[{datetime.utcnow()}] Error: {e}")

        time.sleep(INTERVAL)


if __name__ == "__main__":
    print(f"Monitoring Agent Started (Server ID: {SERVER_ID})")
    send_metrics()