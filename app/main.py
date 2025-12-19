from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import get_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    print(settings.app_name)
    yield


app = FastAPI(
    lifespan=lifespan
)


@app.get("/")
async def root():
    return {"message": "Hello world!"}
