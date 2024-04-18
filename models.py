from pydantic import BaseModel

class Task(BaseModel):
    id: int = None
    title: str
    description: str
    completed: bool = False


