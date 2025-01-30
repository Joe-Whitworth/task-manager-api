from sqlalchemy.orm import Session
from app.db import crud
from app.schemas import task as schemas

def create_task(db: Session, task_data: schemas.TaskCreate):
    return crud.create_task(db, task_data)

def list_tasks(db: Session, completed: bool = None, priority: int = None):
    return crud.get_tasks(db, completed, priority)

def get_task_by_id(db: Session, task_id: int):
    return crud.get_task(db, task_id)

def update_task(db: Session, task_id: int, task_data: schemas.TaskUpdate):
    return crud.update_task(db, task_id, task_data)

def delete_task(db: Session, task_id: int):
    return crud.delete_task(db, task_id)
