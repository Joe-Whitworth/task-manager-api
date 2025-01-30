from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = Field(..., ge=1, le=3, description="Priority must be between 1 (High) and 3 (Low)")
    due_date: datetime

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=3, description="Priority must be between 1 (High) and 3 (Low)")
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None

class TaskResponse(TaskBase):
    id: int
    completed: bool

    class Config:
        from_attributes = True
