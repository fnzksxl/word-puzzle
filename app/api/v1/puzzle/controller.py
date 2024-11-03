from fastapi import APIRouter, status, Depends
from typing import Optional

from .service import PuzzleCreateService, PuzzleReadService, PuzzleHandleService
from .schema import PuzzleSize
from ..auth.dependancy import get_userinfo_from_jwt_must

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
    "/search/{puzzle_id}",
    status_code=status.HTTP_200_OK,
    description="PUZZLE_ID인 십자말풀이판 반환",
)
async def read_puzzle(
    puzzle_id: int, puzzle_service: PuzzleReadService = Depends(PuzzleReadService)
):
    return await puzzle_service.read_puzzle_from_db_by_id(puzzle_id=puzzle_id)


@router.get(
    "/paginated",
    status_code=status.HTTP_200_OK,
    description="MAIN 페이지 데이터 전송, 퍼즐 목록 커서기반 페이지네이션으로 반환",
)
async def read_puzzles_on_main(
    key: Optional[int] = None, puzzle_service: PuzzleReadService = Depends(PuzzleReadService)
):
    return await puzzle_service.get_puzzle_list_by_pagination(key=key)


@router.post("/name/update", status_code=status.HTTP_202_ACCEPTED, description="퍼즐 이름 수정")
async def update_puzzle_name(
    puzzle_id: int,
    name: str,
    user_info: dict = Depends(get_userinfo_from_jwt_must),
    puzzle_service: PuzzleHandleService = Depends(PuzzleHandleService),
):
    return await puzzle_service.set_puzzle_name(puzzle_id=puzzle_id, name=name)
