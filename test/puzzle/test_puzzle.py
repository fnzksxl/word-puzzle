import pytest


@pytest.mark.asyncio
async def test_create_puzzle(client):
    r = await client.get("/puzzle")
    data = r.json()

    assert r.status_code == 200
    assert type(data.get("map", None)) == list


@pytest.mark.asyncio
async def test_create_puzzle_error_with_size(client):
    r = await client.get("/puzzle?size=11")

    assert r.status_code == 422


@pytest.mark.asyncio
async def test_get_puzzle(client, puzzle):
    r = await client.get("/puzzle/search/1")

    assert r.status_code == 200


@pytest.mark.asyncio
async def test_get_puzzle_error_with_wrong_id(client):
    r = await client.get("/puzzle/search/2")

    assert r.status_code == 404


@pytest.mark.asyncio
async def test_get_puzzles_on_main_page(client, four_puzzles):
    r = await client.get("/puzzle/paginated")
    data = r.json()

    assert r.status_code == 200
    assert len(data.get("item", None)) == 4
    assert data.get("next") is None


@pytest.mark.asyncio
async def test_update_puzzle_name(client, token, puzzle):
    cookies = {
        "access": token.get("access", None),
        "refresh": token.get("refresh", None),
    }
    r = await client.post(
        f"/puzzle/name/update?puzzle_id={puzzle.get('id')}&name=new_name", cookies=cookies
    )
    data = r.json()

    assert r.status_code == 202
    assert data.get("name") == "new_name"
