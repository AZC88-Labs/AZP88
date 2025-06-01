from pydantic import BaseModel


class TaskBase(BaseModel):
    """
    Basic Task's pydantic schema.
    """

    title: str
    description: str


    class Config:
        from_attributes = True


class TagBase(BaseModel):
    """
    TODO: IN FUTURE LIKE WHOLE TAG's feature
    Basic Tags pydantic schema.
    """

    class Config:
        from_attributes = True
