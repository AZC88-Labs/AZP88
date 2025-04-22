from datetime import datetime
from .users import User
from ..db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, DateTime, Table, Column, ForeignKey, Enum as SQLEnum
from .enums import TaskRole, TaskTag

task_tags = Table(
    'task_tags',
    Base.metadata,
    Column('task_id', ForeignKey('tasks.id')),
    Column('tag_id', ForeignKey('tags.id'))
)


class Task(Base):
    """
    Represents a task within a project.

    Attributes:
        id (int): Unique identifier for the task.
        project_id (int): Foreign key linking the task to a specific project.
        title (str): Title of the task (up to 255 characters).
        description (str): Detailed description of the task.
        created_at (datetime): Timestamp of when the task was created.

        tags (list[Tag]): Tags assigned to this task via the 'task_tags' association table.
        task_assignees (list[TaskAssignee]): List of user-task-role assignments for this task.
        users_assigned (list[User]): Shortcut relationship to access users assigned to this task.
    """
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('projects.id'),
    )
    title: Mapped[str] = mapped_column(
        String(255)
    )
    description: Mapped[str] = mapped_column(
        Text
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    tags: Mapped[list['Tag']] = relationship(
        'Tag',
        secondary=task_tags,
        back_populates="tasks",
        overlaps='tasks'
    )
    task_assignees: Mapped[list['TaskAssignee']] = relationship(
        'TaskAssignee',
        back_populates="task",
        overlaps='task'
    )
    users_assigned: Mapped[list["User"]] = relationship(
        "User",
        secondary="task_assignees",
        overlaps="task,task_assignees",
    )

class TaskAssignee(Base):
    """
    Association model that links a user to a task with a specific role.

    Attributes:
        user_id (int): ID of the user assigned to the task. Part of the composite primary key.
        task_id (int): ID of the task the user is assigned to. Part of the composite primary key.
        assigned_at (datetime): Timestamp indicating when the user was assigned to the task.
        role (TaskRole): Role of the user within the task context (e.g., owner, reviewer, watcher).

        user (User): Relationship to the User model.
        task (Task): Relationship to the Task model.
    """
    __tablename__ = 'task_assignees'

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id'),
        primary_key=True
    )
    task_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('tasks.id'),
        primary_key=True
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
    role: Mapped[TaskRole] = mapped_column(
        SQLEnum(TaskRole,
                name="task_role",
                create_type=False,
                default=TaskRole.watcher
                ),
    )

    user: Mapped[User] = relationship(
        'User',
        back_populates="task_assignees",
        overlaps='task'
    )
    task: Mapped[Task] = relationship(
        'Task',
        back_populates="task_assignees",
        overlaps="user"
    )


class Tag(Base):
    """
    Represents a tag that can be associated with multiple tasks.

    Attributes:
        id (int): Unique identifier for the tag.
        tag_name (TaskTag): Enum value representing the tag's name/category (e.g., completed, urgent, medium)

        tasks (list[Task]): List of tasks that have this tag, via the 'task_tags' association table.
    """
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    tag_name: Mapped[TaskTag] = mapped_column(
        SQLEnum(TaskTag,
                name="tag_name",
                create_type=False)
    )

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        secondary=task_tags,
        back_populates="tags",
        overlaps="tags"
    )