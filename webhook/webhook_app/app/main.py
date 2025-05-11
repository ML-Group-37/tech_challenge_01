from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import hmac
import hashlib
import os
import docker
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = FastAPI()
security = HTTPBearer()
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
DOCKER_COMPOSE_PATH = "/path/to/your/docker-compose.yml"  # Update this

# Initialize Docker client
docker_client = docker.from_env()

async def verify_webhook(request: Request):
    signature = request.headers.get("X-Hub-Signature-256", "")
    body = await request.body()

    if not WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Server misconfigured")

    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(f"sha256={expected}", signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

    return True

@app.post("/webhook/restart")
async def restart_container(
    request: Request,
    verified: bool = Depends(verify_webhook),
    service_name: str = "your_service"  # Default service name
):
    try:
        # Using docker-compose (requires docker-compose installed on host)
        container = docker_client.containers.get(service_name)
        container.restart()
        return {"status": "success", "message": f"Container {service_name} restarted"}

        # Alternative: Using docker SDK directly
        # containers = docker_client.containers.list(filters={"name": service_name})
        # if containers:
        #     containers[0].restart()
        #     return {"status": "success"}
        # return {"status": "error", "message": "Container not found"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)





from fastapi import FastAPI, Request, HTTPException, Depends
import hmac
import hashlib
import os
import subprocess
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()
security = HTTPBearer()
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
SCRIPT_PATH = "/app/update_script.sh"

async def verify_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256", "")

    if not WEBHOOK_SECRET:
        raise HTTPException(500, "Webhook secret not configured")

    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(f"sha256={expected}", signature):
        raise HTTPException(403, "Invalid signature")

    return True

@app.post("/webhook/update")
async def update_container(
    request: Request,
    verified: bool = Depends(verify_webhook),
    container_name: str = "your_container"  # Default container to update
):
    try:
        result = subprocess.run(
            [SCRIPT_PATH, container_name],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise HTTPException(500, f"Script failed: {result.stderr}")
        return {"status": "success", "output": result.stdout}
    except Exception as e:
        raise HTTPException(500, str(e))