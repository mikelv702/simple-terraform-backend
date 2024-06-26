import logging
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse


from .helpers.local_file_handler import (save_file, 
                                         read_file, 
                                         read_lock_file, 
                                         delete_lock_file, 
                                         save_lock_file)
from .analytics.route import router as analytics_router

from .settings import settings

settings.configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME, 
              version=settings.APP_VERSION, 
              debug=settings.DEBUG)
app.include_router(analytics_router)
# IN MEMORY LOCK FILE! DO NOT USE IN PRODUCTION
lock_info = None

class LockInfo(BaseModel):
    ID: str
    Operation: str
    Info: str
    Who: str
    Version: str
    Created: str
    Path: str

class OutputValue(BaseModel):
    value: Any
    type: Optional[str] = None
    sensitive: Optional[bool] = None

class TerraformState(BaseModel):
    version: int
    terraform_version: str
    serial: int
    lineage: str
    outputs: Dict[str, OutputValue] = Field(default_factory=dict)
    resources: List[Dict[str, Any]] = Field(default_factory=list)
    check_results: Optional[List[Dict[str, Any]]] = None

    class Config:
        extra = "allow"
        
@app.api_route("/tfstate/{project_id}/lock", methods=["LOCK"])
async def lock_state(project_id: int, lock: LockInfo):
    lock_info = read_lock_file(project_id)
    if lock_info is None:
        lock_info = lock
        save_lock_file(project_id, lock_info.model_dump())
        return JSONResponse(content=lock.model_dump(), status_code=200)
    else:
        return JSONResponse(
            content={"error": "State already locked", "locked_by": lock_info.dict()},
            status_code=423
        )

@app.api_route("/tfstate/{project_id}/lock", methods=["UNLOCK"])
async def unlock_state(project_id: int, lock: LockInfo):
    lock_info = read_lock_file(project_id)
    if lock_info is None:
        raise HTTPException(status_code=404, detail="State is not locked")
    if lock_info["ID"] != lock.ID:
        raise HTTPException(status_code=403, detail="Lock ID does not match")
    delete_lock_file(project_id)
    return Response(status_code=200)

@app.get("/tfstate/{project_id}/lock")
async def get_lock(project_id: int):
    lock_info = read_lock_file(project_id)
    if lock_info is None:
        return Response(status_code=404)
    return JSONResponse(content=lock_info.model_dump(), status_code=200)
    
@app.get("/tfstate/{project_id}")
async def get_terraform_state_project(project_id:int):
    logging.info(f"Requesting State File for project {project_id}")
    state_returned = read_file(str(project_id))
    if state_returned is None:
        dummy_state = TerraformState(
            version=4,
            terraform_version="1.0.0",
            serial=1,
            lineage="",
            outputs={
            }
        )
        return dummy_state
    else:
        returned_state = TerraformState(**state_returned)
        return JSONResponse(content=returned_state.model_dump())
    
@app.post("/tfstate/{project_id}")
async def update_terraform_state_project(project_id: int, state: TerraformState):
    logging.info(f"Update state file for project {project_id}")
    save_file(state.model_dump(), str(project_id))
    logging.debug(state)
    return JSONResponse(content=state.model_dump())