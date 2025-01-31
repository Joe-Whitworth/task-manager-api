import uuid
from sqlalchemy import Column, String, Boolean, DateTime
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))    
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=False)
    completed = Column(Boolean, default=False)
