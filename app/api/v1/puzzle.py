from fastapi import APIRouter, status, Depends
from typing import Dict
from app.utils.puzzle import create_puzzle_phase2

router = APIRouter(tags=["PuzzleV1"], prefix="/puzzle")


@router.get("", status_code=status.HTTP_200_OK)
async def create_puzzle(puzzle: Dict = Depends(create_puzzle_phase2)):
    return await puzzle
