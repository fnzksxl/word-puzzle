from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from .jwt import JWTService
from .schema import GeneralRegisterModel, GeneralLoginModel
from .service import GeneralAuthService


def get_general_auth_service_register(
    auth_data: GeneralRegisterModel, db: Session = Depends(get_db)
) -> GeneralAuthService:
    return GeneralAuthService(
        email=auth_data.email, password=auth_data.password, nickname=auth_data.nickname, db=db
    )


def get_general_auth_service_login(
    auth_data: GeneralLoginModel, db: Session = Depends(get_db)
) -> GeneralAuthService:
    return GeneralAuthService(email=auth_data.email, password=auth_data.password, db=db)


def get_userinfo_from_jwt(request: Request, jwt_service: JWTService = Depends(JWTService)):
    cookies = request.cookies
    access_token = cookies.get("access", None)
    if access_token:
        user_info = jwt_service.check_is_expired(access_token)
        user_info.pop("exp")
        return user_info
    return None
