from sqlalchemy.orm import Session
from ..models.users import User
from ..models.projects import Project, ProjectRole as ProjectRoleModel
from ..models.tasks import Task, TaskAssignee
from ..schemas.tasks import TaskBase
from fastapi import HTTPException
from ..models.enums import ProjectRole, TaskRole

def create_task(project_id: int, task_data: TaskBase, db: Session, user: User):
    """
    TODO: Docs
    :param project_id:
    :param task_data:
    :param db:
    :param user:
    :return:
    """

    project = db.query(Project).filter(Project.id==project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    is_owner = user in project.owner_users
    project_role = db.query(ProjectRoleModel).filter_by(
        user_id=user.id, project_id=project.id).first()

    required_roles = [ProjectRole.admin, ProjectRole.watcher]

    if is_owner or project_role in required_roles:
        new_task = Task(
            title=task_data.title,
            description=task_data.description
        )
    else:
        raise HTTPException(status_code=401, detail="Unauthorized operation")

    db.add(new_task)
    db.flush()

    owner_role = TaskAssignee(
        user_id=user.id,
        task_id=new_task.id,
        role=TaskRole.owner
    )

    new_task.task_assignees.append(owner_role)

    db.commit()
    db.refresh(new_task)

    return new_task