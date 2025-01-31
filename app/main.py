from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import engine, Base, database
from app.api.routes import router

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles database connection on startup and shutdown."""
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(
    title="Task Manager API",
    description=(
        "A simple and efficient Task Manager API built with FastAPI.\n\n"
        "Features:\n"
        "- Create, update, delete, and retrieve tasks\n"
        "- Assign priorities and due dates\n"
        "- Mark tasks as complete\n"
        "- Filter tasks by priority and status"
    ),
    version="1.0.0",
    contact={
        "name": "Joe",
        "email": "joe_whitworth@outlook.com",
    },
   
    lifespan=lifespan,  
)

app.include_router(router)
