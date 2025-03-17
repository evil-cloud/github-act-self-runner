from fastapi import FastAPI
import logging
import json
from datetime import datetime, timezone
from prometheus_fastapi_instrumentator import Instrumentator



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("devops")

def log_json(level, component, message, status_code=None):
    log_entry = {
        "level": level,
        "time": datetime.now(timezone.utc).isoformat(),
        "component": component,
        "message": message
    }
    if status_code is not None:
        log_entry["status_code"] = status_code
    print(json.dumps(log_entry))

app = FastAPI()

instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, endpoint="/metrics")

@app.get("/")
async def always_ok():
    log_json("info", "devops", "Service full operated.", 200)
    return {"message": "Hello from devops service v1.0.5"}

@app.get("/health")
async def health_check():
    log_json("info", "devops", "Health check endpoint called.", 200)
    return {"status": "ok", "service": "devops"}
