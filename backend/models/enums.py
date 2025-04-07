from sqlalchemy import Enum

class TeamRole(str, Enum):
    admin = 'admin'
    member = 'member'
    guest = 'guest'
    pending = 'pending'


class ProjectRole(str, Enum):
    admin = 'admin'
    contributor = 'contributor'
    watcher = 'watcher'


class TaskRole(str, Enum):
    owner = 'owner'
    assignee = 'assignee'
    reviewer = 'reviewer'
    watcher = 'watcher'


class TaskTag(str, Enum):
    urgent = 'urgent'
    high = 'high'
    medium = 'medium'
    low = 'low'
    completed = 'completed'


class UserRole(str, Enum):
    admin = 'admin'
    user = 'user'
