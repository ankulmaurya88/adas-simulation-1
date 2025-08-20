# services/tpms-service/app/views/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="tpms-service")
# app.state.orchestrator will be set in main

class RunReq(BaseModel):
    action: Optional[str] = "step"  # step/start/stop (start/stop not implemented in this minimal example)

@app.post("/run")
def run(req: RunReq):
    try:
        orch = app.state.orchestrator
        result = orch.controllers["tpms"].step()
        return {"ok": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status":"ok"}
