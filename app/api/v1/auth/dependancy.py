from fastapi import Depends, Request
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from .exception import TokenExpiredException, TokenNotExistException
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


def get_userinfo(request: Request, jwt_service: JWTService = Depends(JWTService)):
    cookies = request.cookies
    access_token = cookies.get("access", None)
    refresh_token = cookies.get("refresh", None)
    if access_token and refresh_token:
        user_info = jwt_service.check_is_expired(access_token)
        if user_info:
            user_info.pop("exp")
            return user_info
        else:
            raise TokenExpiredException()
    else:
        return None


def get_userinfo_from_jwt_must(user_info: dict = Depends(get_userinfo)) -> Optional[dict]:
    if user_info:
        return user_info
    raise TokenNotExistException()


def get_userinfo_from_jwt_not_must(user_info: dict = Depends(get_userinfo)) -> Optional[dict]:
    if user_info:
        return user_info
    return {"id": 0}
