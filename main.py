from fastapi import FastAPI, HTTPException
from models import Task
import sqlite3

app = FastAPI()

conn = sqlite3.connect('tasks.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT,
             description TEXT,
             completed BOOLEAN default FALSE
             )'''
        )
conn.commit()

@app.post("/tasks")
async def create_task(task: Task):
    """
    Create a new task.

    Parameters:
    - task (Task): The task object containing title, description, and completed status.

    Returns:
    - Task: The created task object.
    """

    c.execute("INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)", (task.title, task.description, task.completed))
    conn.commit()
    return task

@app.get("/tasks")
async def get_tasks():
    """
    Get all tasks.

    Returns:
    - List[Task]: A list of all task objects.
    """

    c.execute("SELECT * FROM tasks")
    rows = c.fetchall()
    tasks = []
    for row in rows:
        task = Task(id=row[0], title=row[1], description=row[2], completed=bool(row[3]))
        tasks.append(task)
    return tasks 

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    """
    Get a task by its ID.

    Parameters:
    - task_id (int): The ID of the task to retrieve.

    Returns:
    - Task: The task object corresponding to the given ID.

    Raises:
    - HTTPException(404): If the task with the given ID is not found.
    """

    c.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    row = c.fetchone()
    if row:
        return Task(id=row[0], title=row[1], description=row[2], completed=bool(row[3]))
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, updated_task: Task):
    """
    Update a task by its ID.

    Parameters:
    - task_id (int): The ID of the task to update.
    - updated_task (Task): The updated task object containing new title, description, and completed status.

    Returns:
    - Task: The updated task object.

    Raises:
    - HTTPException(404): If the task with the given ID is not found.
    """

    c.execute("UPDATE tasks SET title=?, description=?, completed=? WHERE id=?", (updated_task.title, updated_task.description, updated_task.completed, task_id))
    conn.commit()
    if c.rowcount > 0:
        return updated_task
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """
    Delete a task by its ID.

    Parameters:
    - task_id (int): The ID of the task to delete.

    Returns:
    - Dict[str, str]: A message confirming successful deletion.

    Raises:
    - HTTPException(404): If the task with the given ID is not found.
    """
    
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    if c.rowcount > 0:
        return {"message": "Task deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Task not found")

