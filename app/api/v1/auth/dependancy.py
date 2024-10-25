from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
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
