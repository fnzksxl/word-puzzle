import pytest_asyncio
from datetime import datetime
from jose import jwt
from zoneinfo import ZoneInfo

from app import models
from app.api.v1.auth.jwt import JWTService


@pytest_asyncio.fixture
async def expired_token(user):
    jwt_service = JWTService()
    user_dict = user.as_dict()
    user_dict.pop("password")
    user_dict.pop("created_at")
    user_dict.pop("updated_at")

    expire = datetime.now(ZoneInfo("Asia/Seoul"))
    refresh_token = jwt_service.create_refresh_token(user_dict)
    user_dict.update({"exp": expire})
    access_token = jwt.encode(user_dict, jwt_service.secret_key, algorithm=jwt_service.algorithm)

    return {"access": access_token, "refresh": refresh_token}


@pytest_asyncio.fixture
async def oauth_google_user(session):
    user = models.User(email="test@test.com", nickname="test")
    session.add(user)
    session.flush()

    oauth_info = models.OAuth(user_id=user.id, email=user.email, provider="google")
    session.add(oauth_info)
    session.commit()
