from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import get_settings
from app.core.logging import setup_logging
from loguru import logger


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    setup_logging()
    logger.info(f"Running App: {settings.app_name}")
    yield


app = FastAPI(
    lifespan=lifespan
)


@app.get("/")
async def root():
    return {"message": "Hello world!"}
