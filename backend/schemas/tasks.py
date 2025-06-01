from pydantic import BaseModel, field_validator


class TaskBase(BaseModel):
    """
    Basic Task's Pydantic schema.

    Attributes:
        title (str): The title of the task. Must be between 3 and 255 characters long.
        description (str): The description of the task. Must not exceed 1000 characters.
    """

    title: str
    description: str

    @field_validator('title')
    def validate_title(cls, title: str) -> str:
        """
        Validates the 'title' field.

        Ensures that:
        - The title is stripped of leading and trailing whitespace.
        - The title is at least 3 characters long.
        - The title does not exceed 255 characters.

        Args:
            title (str): The title to validate.

        Returns:
            str: The validated and stripped title.

        Raises:
            ValueError: If the title is too short or too long.
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
        Validates the 'description' field.

        Ensures that:
        - The description is stripped of leading and trailing whitespace.
        - The description does not exceed 1000 characters.

        Args:
            description (str): The description to validate.

        Returns:
            str: The validated and stripped description.

        Raises:
            ValueError: If the description exceeds 1000 characters.
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
