from pydantic import BaseModel


class TaskBase(BaseModel):
    """
    Basic Task's pydantic schema.
    """

    class Config:
        from_attributes = True


class TaskCreate(TaskBase):
    """
    TODO: documentation, validation
    """

    title: str
    description: str


class TaskEdit(TaskBase):
    """
    TODO: documentation, validation
    """

    title: str
    description: str


class TaskDelete(TaskBase):
    """
    TODO: documentation, validation
    """

    title: str
    description: str


class TagBase(BaseModel):
    """
    Basic Tags pydantic schema.
    """

    class Config:
        from_attributes = True


class TagCreate(TagBase):
    """
    TODO: documentation, validation
    """

    tag_name: str


class TagEdit(TagBase):
    """
    TODO: documentation, validation
    """

    tag_name: str


class TagDelete(TagBase):
    """
    TODO: documentation, validation
    """
    tag_name: str
