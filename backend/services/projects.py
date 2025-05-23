from fastapi import Depends
from sqlalchemy.orm import Session
from ..dependencies import get_current_user, get_db
from ..models.users import User
from ..schemas.projects import ProjectBase
from ..models.projects import Project, ProjectRole


# FOR USER. IN FUTURE REFACTOR AND ADD LOGIC FOR TEAMS!
def create_project(project_data: ProjectBase, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    Creates a new project and assigns the current user as its owner with the admin role.

    Args:
        project_data (ProjectBase): Data for the new project (title, description, etc.).
        db (Session): SQLAlchemy database session, injected by FastAPI.
        user (User): The current authenticated user, injected by FastAPI.

    Returns:
        Project: The newly created project instance, refreshed from the database.
    """

    new_project = Project(
        title=project_data.title,
        description=project_data.description,
        owner_users=[user]
    )

    db.add(new_project)
    db.flush()

    owner_role = ProjectRole(
        user_id=user.id,
        project_id=new_project.id,
        role=ProjectRole.admin
    )

    new_project.project_roles.append(owner_role)

    db.commit()
    db.refresh(new_project)

    return new_project
