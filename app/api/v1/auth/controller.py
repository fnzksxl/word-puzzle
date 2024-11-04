from fastapi import APIRouter, status, Depends

from .service import GeneralAuthService, GoogleOAuthService, AuthHelper
from .dependancy import (
    get_general_auth_service_login,
    get_general_auth_service_register,
    get_userinfo_from_jwt_must,
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
async def google_callback(auth_service: GoogleOAuthService = Depends(GoogleOAuthService)):
    return await auth_service.login()


@router.get("/duplicated", status_code=status.HTTP_200_OK, description="이메일 중복 확인")
async def is_duplicated_email(email: str, auth_service: AuthHelper = Depends(AuthHelper)):
    return await auth_service.is_duplicated(email)


@router.get("/get-user", status_code=status.HTTP_200_OK, description="JWt 기반으로 유저 정보 반환")
async def get_user_by_jwt(user: dict = Depends(get_userinfo_from_jwt_must)):
    return user


@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT, description="로그아웃")
async def logout(auth_service: AuthHelper = Depends(AuthHelper)):
    return await auth_service.logout()
