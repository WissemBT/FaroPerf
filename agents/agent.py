import json
import os
import time
import psutil
import socket
import requests
from datetime import datetime, timezone


CONF_PATH = os.getenv("FARO_CONF", "/tmp/faro-conf.json")
INTERVAL  = int(os.getenv("FARO_INTERVAL", "20"))


def load_conf():
    with open(CONF_PATH) as f:
        cfg = json.load(f)
    return cfg["backend_url"], cfg["server_id"], cfg["api_key"]


def collect_metrics():
    return {
        "timestamp"   : datetime.now(timezone.utc).isoformat(),
        "cpu_usage"   : psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage"  : psutil.disk_usage('/').percent,
        "network_in"  : psutil.net_io_counters().bytes_recv / (1024*1024),
        "network_out" : psutil.net_io_counters().bytes_sent / (1024*1024),
    }


def main():
    backend, server_id, api_key = load_conf()
    headers = {"X-API-Key": api_key, "Content-Type": "application/json"}

    print(f"Agent started for server {server_id} (interval {INTERVAL}s)")

    while True:
        payload = collect_metrics()
        try:
            r = requests.post(f"{backend}/metrics", json=payload, headers=headers, timeout=5)
            if r.status_code == 201:
                print(f"[{datetime.utcnow()}] Metrics OK")
            else:
                print(f"[{datetime.utcnow()}] Error {r.status_code}: {r.text}")
        except Exception as exc:
            print(f"[{datetime.utcnow()}] Network error: {exc}")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
