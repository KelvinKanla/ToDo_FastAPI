from pydantic import BaseModel

class Task(BaseModel):
    """
    Represents a task object.

    Attributes:
    - id (int, auto-generated): The unique identifier for the task.
    - title (str): The title of the task.
    - description (str): The description of the task.
    - completed (bool, default=False): Indicates whether the task is completed.
    """

    id: int = None
    title: str
    description: str
    completed: bool = False


