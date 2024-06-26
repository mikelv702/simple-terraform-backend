import logging
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse


from .helpers.local_file_handler import save_file, read_file

from .settings import settings

settings.configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME, 
              version=settings.APP_VERSION, 
              debug=settings.DEBUG)

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
@app.api_route("/tfstate/lock", methods=["LOCK"])
async def lock_state(lock: LockInfo):
    global lock_info
    if lock_info is None:
        lock_info = lock
        return JSONResponse(content=lock.model_dump(), status_code=200)
    else:
        return JSONResponse(
            content={"error": "State already locked", "locked_by": lock_info.dict()},
            status_code=423
        )

@app.api_route("/tfstate/lock", methods=["UNLOCK"])
async def unlock_state(lock: LockInfo):
    global lock_info
    if lock_info is None:
        raise HTTPException(status_code=404, detail="State is not locked")
    if lock_info.ID != lock.ID:
        raise HTTPException(status_code=403, detail="Lock ID does not match")
    lock_info = None
    return Response(status_code=200)

@app.get("/tfstate/lock")
async def get_lock():
    if lock_info is None:
        return Response(status_code=404)
    return JSONResponse(content=lock_info.model_dump(), status_code=200)

@app.post("/tfstate")
async def update_terraform_state(ID: str, state: TerraformState):
    logging.info(f"Update state file {ID}")
    save_file(state.model_dump())
    logging.debug(state)
    return JSONResponse(content=state.model_dump())

@app.get("/tfstate")
async def get_terraform_state():
    logging.info("Requesting State File")
    state_returned = read_file()
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