from fastapi import APIRouter, status, Depends
from .service import PuzzleCreateService, PuzzleReadService
from .schema import PuzzleSize

router = APIRouter(tags=["PuzzleV1"], prefix="/puzzle")


@router.get(
    "", status_code=status.HTTP_200_OK, description="[SIZE x SIZE] 크기의 십자말풀이판 생성해 반환"
)
async def create_puzzle(
    puzzle_size: PuzzleSize = Depends(),
    puzzle_service: PuzzleCreateService = Depends(PuzzleCreateService),
):
    puzzle = await puzzle_service.create_puzzle_phase3()
    await puzzle_service.insert_map_answer_into_db()

    return puzzle


@router.get(
    "/{puzzle_id}", status_code=status.HTTP_200_OK, description="PUZZLE_ID인 십자말풀이판 반환"
)
async def read_puzzle(
    puzzle_id: int, puzzle_service: PuzzleReadService = Depends(PuzzleReadService)
):
    return await puzzle_service.read_puzzle_from_db_by_id()
