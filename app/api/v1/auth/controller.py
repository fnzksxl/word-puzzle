from fastapi import APIRouter, status, Depends

from .service import GeneralAuthService, GoogleOAuthService
from .dependancy import (
    get_general_auth_service_login,
    get_general_auth_service_register,
    get_userinfo_from_jwt,
)

router = APIRouter(tags=["AuthV1"], prefix="/auth")


@router.post(
    "/general-register", status_code=status.HTTP_201_CREATED, description="EMAIL/PW로 가입"
)
async def general_register(
    auth_service: GeneralAuthService = Depends(get_general_auth_service_register),
):
    return await auth_service.register()


@router.post("/general-login", status_code=status.HTTP_200_OK, description="EMAIL/PW로 로그인")
async def general_login(auth_service: GeneralAuthService = Depends(get_general_auth_service_login)):
    return await auth_service.login()


@router.get(
    "/oauth-register/google/callback",
    status_code=status.HTTP_201_CREATED,
    description="구글 소셜 로그인",
)
async def kakao_callback(auth_service: GoogleOAuthService = Depends(GoogleOAuthService)):
    return await auth_service.login()


@router.get("/get-user", status_code=status.HTTP_200_OK, description="JWt 기반으로 유저 정보 반환")
async def get_user_by_jwt(user: dict = Depends(get_userinfo_from_jwt)):
    return user
