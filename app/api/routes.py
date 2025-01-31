from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db import crud
from app.schemas.tasks import TaskCreate, TaskUpdate, TaskResponse
from uuid import UUID

router = APIRouter()

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tasks/", response_model=TaskResponse, summary="Create a Task", description="Creates a new task with title, description, priority, and due date.")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    return crud.create_task(db, task)

@router.get("/tasks/", response_model=list[TaskResponse], summary="List Tasks", description="Retrieves a list of tasks, with optional filters for completion status and priority.")
def get_tasks(completed: bool = None, priority: int = None, db: Session = Depends(get_db)):
    """Fetch all tasks with optional filtering by completion status and priority."""
    return crud.get_tasks(db, completed, priority)

@router.get("/tasks/{task_id}/", response_model=TaskResponse, summary="Get a Task", description="Retrieves a task by its unique ID.")
def get_task(task_id: UUID, db: Session = Depends(get_db)):
    """Get a specific task by ID."""
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}/", response_model=TaskResponse, summary="Update a Task", description="Updates an existing task by ID. You can modify title, description, priority, due date, or completion status.")
def update_task(task_id: UUID, task: TaskUpdate, db: Session = Depends(get_db)):
    """Update an existing task by ID."""
    return crud.update_task(db, task_id, task)

@router.delete("/tasks/{task_id}/", summary="Delete a Task", description="Deletes a task by ID.")
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    """Delete a task by ID."""
    if not crud.delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully."}
