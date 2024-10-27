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
    r = await client.get("/puzzle/1")

    assert r.status_code == 200


@pytest.mark.asyncio
async def test_get_puzzle_error_with_wrong_id(client):
    r = await client.get("/puzzle/2")

    assert r.status_code == 404
