from fastapi import FastAPI
from routes.server import router as server_router
from routes.metric import router as metric_router
from routes.alert import router as alert_router
from routes.alert_rules import router as alert_rules_router
from routes.user import router as user_router
from routes.notification import router as notification_router
from routes.auth import router as auth_router
from routes.api_keys import router as api_keys_router

app = FastAPI()

app.include_router(server_router)
app.include_router(metric_router)
app.include_router(alert_router)
app.include_router(alert_rules_router)
app.include_router(user_router)
app.include_router(notification_router)
app.include_router(auth_router)
app.include_router(api_keys_router)


@app.get("/")
def home():
    return {"message": "Faro is running"}