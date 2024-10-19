from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import time

from app.api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app import models
    from app.database import engine

    models.Base.metadata.create_all(bind=engine)

    yield

    pass


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response
