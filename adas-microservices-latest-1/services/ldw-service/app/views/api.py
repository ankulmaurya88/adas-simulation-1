# services/ldw-service/app/views/api.py
from fastapi import APIRouter, HTTPException
from app.utils.exceptions import ADASException
from app.utils.logger import logger

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/run")
def run_step(controller):
    try:
        result = controller.step()
        return {"success": True, "data": result}
    except ADASException as ae:
        logger.error("ADAS error: %s", ae)
        raise HTTPException(status_code=500, detail=str(ae))
    except Exception as e:
        logger.exception("Unexpected error in /run")
        raise HTTPException(status_code=500, detail="Internal server error")
