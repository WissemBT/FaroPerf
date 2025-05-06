# FaroPerf

## Overview
FaroPerf is a FastAPI-based backend system that allows users to monitor multiple servers, collect metrics, trigger and resolve alerts based on customized rules, for the moment it is quite simple, looking up for a better solution in the Future.

## Prerequisites
Before testing, ensure the following are installed and running:

1. PostgreSQL (configured via DATABASE_URL in .env or database.py)

2. Redis (used for Celery broker/backend)

3. Python 3.10+

4. Virtual environment activated with all dependencies installed

5. Alembic migrations applied

## Launching the system
### 1. Start Postgresql and Redis
Make sure that postgresql and redis server are up:
```bash
sudo systemctl start postgresql
sudo systemctl start redis-server
```

### 2. Activate Virtual Environment
```bash
cd FaroPerf
source env/bin/activate
```

### 3. Apply alembic migrations (if needed)
```bash
alembic upgrade head
```

### Start Backend server
```bash
uvicorn main:app --reload
```
Runs at localhost:8000

### Start Celery worker and beat
```bash
celery -A celery_worker worker --loglevel=info
celery -A celery_worker beat --loglevel=info
```