import pytest
import json
from unittest.mock import patch

from test.auth import mock
from app import models


@pytest.mark.asyncio
async def test_general_register(client, session):
    body = {
        "email": "test@test.com",
        "password": "test1234",
        "nickname": "testname",
    }
    r = await client.post("/auth/general-register", data=json.dumps(body))

    assert r.status_code == 200

    user = session.query(models.User).filter(models.User.email == body.get("email")).first()

    assert body.get("email") == user.email
    assert body.get("nickname") == user.nickname


@pytest.mark.asyncio
async def test_general_login(client, user):
    body = {"email": "test@test.com", "password": "test1234"}
    r = await client.post("/auth/general-login", data=json.dumps(body))

    assert r.status_code == 200


@pytest.mark.asyncio
async def test_get_user_by_token(client, token):
    cookies = {"access": token}
    r = await client.get("/auth/get-user", cookies=cookies)
    data = r.json()

    assert r.status_code == 200
    assert data.get("email", None) == "test@test.com"


@pytest.mark.asyncio
@patch("app.api.v1.auth.service.GoogleOAuthService.get_token", new=mock.mock_post_token_request)
@patch("app.api.v1.auth.service.GoogleOAuthService.get_userinfo", new=mock.mock_get_userinfo)
async def test_google_register(client, session):
    code = "dummy code"
    r = await client.get(f"/auth/oauth-register/google/callback?code={code}")

    assert r.status_code == 200

    user = session.query(models.User).filter(models.User.email == "test@test.com").first()

    assert "test" == user.nickname

    oauth_user = session.query(models.OAuth).filter(models.OAuth.id == user.id).first()

    assert oauth_user.email == user.email


@pytest.mark.asyncio
@patch("app.api.v1.auth.service.GoogleOAuthService.get_token", new=mock.mock_post_token_request)
@patch("app.api.v1.auth.service.GoogleOAuthService.get_userinfo", new=mock.mock_get_userinfo)
async def test_google_login(client, oauth_google_user):
    code = "dummmy code"
    r = await client.get(f"/auth/oauth-register/google/callback?code={code}")
    data = r.json()

    assert r.status_code == 200
    assert data.get("email") == "test@test.com"
    assert data.get("nickname") == "test"
