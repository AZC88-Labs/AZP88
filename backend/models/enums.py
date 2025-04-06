from sqlalchemy import enum


class TeamRole(str, enum.Enum):
    admin = 'admin'
    member = 'member'
    guest = 'guest'
    pending = 'pending'


class ProjectRole(str, enum.Enum):
    admin = 'admin'
    contributor = 'contributor'
    watcher = 'watcher'


class TaskRole(str, enum.Enum):
    owner = 'owner'
    assignee = 'assignee'
    reviewer = 'reviewer'
    watcher = 'watcher'


class TaskTag(str, enum.Enum):
    urgent = 'urgent'
    high = 'high'
    medium = 'medium'
    low = 'low'
    completed = 'completed'


class UserRole(str, enum.Enum):
    admin = 'admin'
    user = 'user'
