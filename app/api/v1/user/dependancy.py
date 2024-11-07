from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from .service import ProfileService
from ..auth.dependancy import get_userinfo_from_jwt_must


def get_profile_service(
    userinfo: dict = Depends(get_userinfo_from_jwt_must), db: Session = Depends(get_db)
):
    return ProfileService(user=userinfo, db=db)
