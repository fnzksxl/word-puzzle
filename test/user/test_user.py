import pytest


@pytest.mark.asyncio
async def test_user_solved_update(client, puzzle, token):
    cookies = {
        "access": token.get("access", None),
        "refresh": token.get("refresh", None),
    }
    r = await client.post(f"/user/update/solved?puzzle_id={puzzle['id']}", cookies=cookies)
    data = r.json()

    assert r.status_code == 202
    assert data["solved"] == 1
