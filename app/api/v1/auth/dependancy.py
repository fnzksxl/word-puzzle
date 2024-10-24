from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from .schema import GeneralAuthModel
from .service import GeneralAuthService


def get_general_auth_service(
    auth_data: GeneralAuthModel, db: Session = Depends(get_db)
) -> GeneralAuthService:
    return GeneralAuthService(
        email=auth_data.email, password=auth_data.password, nickname=auth_data.nickname, db=db
    )
