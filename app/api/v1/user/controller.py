from fastapi import APIRouter, Depends, status

from .dependancy import get_profile_service
from .service import ProfileService

router = APIRouter(tags=["UserV1"], prefix="/user")


@router.post(
    "/update/solved", status_code=status.HTTP_202_ACCEPTED, description="유저 solved 개수 업데이트"
)
async def update_solved_count(
    puzzle_id: int, profile_service: ProfileService = Depends(get_profile_service)
):
    return await profile_service.update_solved_count(puzzle_id=puzzle_id)
