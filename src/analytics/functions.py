from .models import ProjectAnalytics
from ..helpers.local_file_handler import read_file, read_lock_file


def get_project_analytics(project_id):
    state_file = read_file(project_id=str(project_id))
    lock_file = read_lock_file(project_id=project_id)
    if lock_file is None:
        locked = False
    else:
        locked = True
    if state_file is None:
        project_analytics = ProjectAnalytics(
            project_id= project_id,
            resource_count= 0, 
            locked=locked
        )
        return project_analytics
    else:
        project_analytics = ProjectAnalytics(
            project_id= project_id,
            resource_count= len(state_file['resources']), 
            locked=locked
        )
        return project_analytics