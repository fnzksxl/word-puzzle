async def mock_get_userinfo(*args, **kwargs):
    return {"email": "test@test.com", "name": "testuser"}


async def mock_post_token_request(*args, **kwargs):
    return {"access_token": "mock_access_token"}
