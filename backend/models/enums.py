from enum import Enum


class TeamRole(str, Enum):
    """
    Enum representing possible roles of a user in a team.
    """
    admin = 'admin'
    member = 'member'
    guest = 'guest'
    pending = 'pending'


class ProjectRole(str, Enum):
    """
    Enum representing possible roles of a user in a project.
    """
    admin = 'admin'
    contributor = 'contributor'
    watcher = 'watcher'


class TaskRole(str, Enum):
    """
    Enum representing possible roles of a user in a task.
    """
    owner = 'owner'
    assignee = 'assignee'
    reviewer = 'reviewer'
    watcher = 'watcher'


class TaskTag(str, Enum):
    """
    Enum representing possible tags of a task.
    """
    urgent = 'urgent'
    high = 'high'
    medium = 'medium'
    low = 'low'
    completed = 'completed'


class UserRole(str, Enum):
    """
    Enum representing possible roles of a user.
    """
    admin = 'admin'
    user = 'user'
