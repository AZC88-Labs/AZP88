from requests import Session
from ..dependencies import get_current_user
from ..db import get_db
from fastapi import Depends, APIRouter
from ..models.users import User
from ..schemas.tasks import TaskBase
from ..services.tasks import create_task

router = APIRouter()


@router.put(
    "/create",
    summary="Creates a new task in the project",
    description="Endpoint allows you to create a new task within the selected project based on the provided data.",
    tags=["Tasks"]
)
def create(project_id: int, task_data: TaskBase, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    Creates a new task within a specified project.

    Args:
        project_id (int): The ID of the project to which the task will be added.
        task_data (TaskBase): The data for the new task, including its attributes.
        db (Session): The database session dependency.
        user (User): The currently authenticated user dependency.

    Returns:
        Task: The newly created task object.
    """

    new_task = create_task(project_id, task_data, db, user)
    return new_task
