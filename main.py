from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse

from .helpers.local_file_handler import save_file, read_file

app = FastAPI()


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
    print("Update State File")
    print(ID)


    save_file(state.model_dump())
    print(state)
    return JSONResponse(content=state.model_dump())

@app.get("/tfstate")
async def get_terraform_state():
    print("Getting State File")
    # Here you would typically retrieve the state from your storage system
    # For this example, we'll just return a dummy state
    state_returned = read_file()
    if len(state_returned) < 4:
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
        dummy_state = TerraformState(**state_returned)

        print(dummy_state)
        return JSONResponse(content=dummy_state.model_dump())