from fastapi import APIRouter
from .puzzle import router as puzzle_router

router = APIRouter()

router.include_router(puzzle_router, prefix="/v1")
