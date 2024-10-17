from fastapi import APIRouter, status, Depends
from typing import Dict
from app.utils.puzzle import PuzzleCreateService

router = APIRouter(tags=["PuzzleV1"], prefix="/puzzle")


@router.get("", status_code=status.HTTP_200_OK)
async def create_puzzle(puzzle: Dict = Depends(PuzzleCreateService)):
    return puzzle
