from pydantic import BaseModel, field_validator


class TaskBase(BaseModel):
    """
    Basic Task's pydantic schema.
    """

    title: str
    description: str

    @field_validator('title')
    def validate_title(cls, title: str) -> str:
        """
        TODO
        :param title:
        :return:
        """
        title = title.strip()
        if len(title) < 3:
            raise ValueError("Task title must be at least 3 characters long")
        if len(title) > 255:
            raise ValueError("Task title must be at most 255 characters long")
        return title

    @field_validator('description')
    def validate_description(cls, description: str) -> str:
        """
        TODO
        :param description:
        :return:
        """
        description = description.strip()
        if len(description) > 1000:
            raise ValueError("Description must be at most 1000 characters long")
        return description

    class Config:
        from_attributes = True


class TagBase(BaseModel):
    """
    TODO: IN FUTURE LIKE WHOLE TAG's feature
    Basic Tags pydantic schema.
    """

    class Config:
        from_attributes = True
