from contextlib import asynccontextmanager
from fastapi import FastAPI

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app import models
    from app.database import engine

    models.Base.metadata.create_all(bind=engine)

    yield

    pass
