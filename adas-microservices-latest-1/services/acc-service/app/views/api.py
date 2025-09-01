# services/acc-service/app/views/api.py
from fastapi import APIRouter, HTTPException
from app.utils.logger import logger
from app.utils.exceptions import ADASException

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/run")
def run_step():
    """
    Trigger a single step. The controller is injected into app.state.controller in main.py
    """
    from fastapi import Request
    # We'll get controller from the FastAPI app state at runtime in main.py where router is included.
    raise HTTPException(status_code=501, detail="This endpoint is a placeholder. Use POST /run on mounted app.")
