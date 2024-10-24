from fastapi import APIRouter, status, Depends

from .service import GeneralAuthService
from .dependancy import get_general_auth_service

router = APIRouter(tags=["AuthV1"], prefix="/auth")


@router.post(
    "/general-register", status_code=status.HTTP_201_CREATED, description="EMAIL/PW로 가입"
)
async def general_register(auth_service: GeneralAuthService = Depends(get_general_auth_service)):
    return await auth_service.register()


@router.post("/general-login", status_code=status.HTTP_200_OK, description="EMAIL/PW로 로그인")
async def general_login(auth_service: GeneralAuthService = Depends(get_general_auth_service)):
    return await auth_service.login()
