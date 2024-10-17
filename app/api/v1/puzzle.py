from fastapi import APIRouter, status, Depends
from app.utils.puzzle import PuzzleCreateService

router = APIRouter(tags=["PuzzleV1"], prefix="/puzzle")


@router.get("", status_code=status.HTTP_200_OK)
async def create_puzzle(puzzle: PuzzleCreateService = Depends(PuzzleCreateService)):
    return await puzzle.create_puzzle_phase3()
