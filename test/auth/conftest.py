import bcrypt
import pytest_asyncio

from app import models
from app.api.v1.auth.jwt import JWTService


@pytest_asyncio.fixture
async def user(session):
    user_dict = {
        "email": "test@test.com",
        "nickname": "testname",
    }
    raw_password = "test1234"
    salt_value = bcrypt.gensalt()
    password = bcrypt.hashpw(raw_password.encode(), salt_value)

    user_dict.update({"password": password})

    user_row = models.User(**user_dict)
    session.add(user_row)
    session.commit()

    return user_row


@pytest_asyncio.fixture
async def token(user):
    jwt_service = JWTService()
    user_dict = user.as_dict()
    user_dict.pop("password")
    user_dict.pop("created_at")
    user_dict.pop("updated_at")
    access_token = jwt_service.create_access_token(user_dict)

    return access_token


@pytest_asyncio.fixture
async def oauth_google_user(session):
    user = models.User(email="test@test.com", nickname="test")
    session.add(user)
    session.flush()

    oauth_info = models.OAuth(user_id=user.id, email=user.email, provider="google")
    session.add(oauth_info)
    session.commit()
