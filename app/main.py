from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import engine, Base, database
from app.api.routes import router

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(router)
