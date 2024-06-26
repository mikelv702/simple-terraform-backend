from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .functions import get_project_analytics

router = APIRouter(prefix="/analytics",tags=["Analytics", "Project Analytics"])


@router.get("/{project_id}")
def get_analytics(project_id: int):
    analytics = get_project_analytics(project_id=project_id)
    return JSONResponse(analytics.model_dump(), status_code=200)
    
