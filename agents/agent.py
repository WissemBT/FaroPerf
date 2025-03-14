import psutil
import requests
import time
import socket
from datetime import datetime
import uuid


BACKEND_URL = "http://127.0.0.1:8000"
INTERVAL = 20  # Send metrics every 20 seconds


def get_system_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return hostname, ip_address


def register_server():
    hostname, ip_address = get_system_info()

    response = requests.get(f"{BACKEND_URL}/servers/")
    if response.status_code == 200:
        servers = response.json()
        for server in servers:
            if server["ip_address"] == ip_address:
                print(f"Server already registered: {server['server_id']}")
                return server["server_id"]

    data = {"hostname": hostname, "ip_address": ip_address}
    response = requests.post(f"{BACKEND_URL}/servers/", json=data)

    if response.status_code == 201:
        server_id = response.json()["server_id"]
        print(f"Server registered successfully! ID: {server_id}")
        return server_id
    else:
        print(f"Failed to register server: {response.text}")
        return None


def collect_metrics(server_id):
    """Collect system metrics using psutil."""
    return {
        "server_id": server_id,
        "timestamp": datetime.utcnow().isoformat(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "network_in": psutil.net_io_counters().bytes_recv / (1024 * 1024),  # MB
        "network_out": psutil.net_io_counters().bytes_sent / (1024 * 1024)  # MB
    }


def send_metrics():
    server_id = register_server()
    if not server_id:
        print("Exiting: Could not get server ID")
        return

    while True:
        try:
            data = collect_metrics(server_id)
            response = requests.post(f"{BACKEND_URL}/metrics/", json=data)

            if response.status_code == 201:
                print(f"[{datetime.utcnow()}] Metrics sent successfully")
            else:
                print(f"[{datetime.utcnow()}] Failed to send metrics: {response.text}")

        except Exception as e:
            print(f"[{datetime.utcnow()}] Error: {e}")

        time.sleep(INTERVAL)

if __name__ == "__main__":
    print("Monitoring Agent Started")
    send_metrics()
