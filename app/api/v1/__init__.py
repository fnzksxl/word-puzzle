from fastapi import APIRouter
from .puzzle.controller import router as puzzle_router
from .auth.controller import router as auth_router

router = APIRouter()

router.include_router(puzzle_router, prefix="/v1")
router.include_router(auth_router, prefix="/v1")
