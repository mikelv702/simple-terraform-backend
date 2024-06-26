from pydantic import BaseModel


class ProjectAnalytics(BaseModel):
    project_id: int
    resource_count: int
    locked: bool
    