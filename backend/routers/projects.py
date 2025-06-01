from requests import Session
from ..dependencies import get_current_user
from ..db import get_db
from fastapi import Depends, APIRouter
from ..models.users import User
from ..schemas.projects import ProjectBase
from ..services.projects import create_project

router = APIRouter()


@router.put(
    "/create",
    summary="Creates new project",
    description="Endpoint allows you to create a new project based on the provided data. Requires authentication.",
    tags=["projects"]
)
def create(project_data: ProjectBase, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    Creates a new project.

    Args:
        project_data (ProjectBase): The data required to create a new project.
        db (Session): Database session dependency.
        user (User): The currently authenticated user.

    Returns:
        Project: The newly created project object.
    """

    new_project = create_project(project_data, db, user)
    return new_project
