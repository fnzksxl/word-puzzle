import pytest_asyncio
import json

from app import models


@pytest_asyncio.fixture
async def puzzle(session):
    with open("test/example/example_map.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    _map = json_data.get("map", None)
    _answers = json_data.get("desc", None)

    map_row = models.Puzzle(puzzle=_map, is_exposed=True)
    session.add(map_row)
    session.flush()

    insert_data = [
        {"puzzle_id": map_row.id, "word_id": desc["id"], "num": desc["num"]} for desc in _answers
    ]

    session.bulk_insert_mappings(models.PuzzleAnswer, insert_data)
    session.commit()

    return {"id": map_row.id, "name": map_row.name}


@pytest_asyncio.fixture
async def four_puzzles(session):
    with open("test/example/example_map.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    _map = json_data.get("map", None)
    _answers = json_data.get("desc", None)
    for _ in range(4):
        map_row = models.Puzzle(puzzle=_map, is_exposed=True)
        session.add(map_row)
        session.flush()

        insert_data = [
            {"puzzle_id": map_row.id, "word_id": desc["id"], "num": desc["num"]}
            for desc in _answers
        ]

        session.bulk_insert_mappings(models.PuzzleAnswer, insert_data)
        session.commit()


@pytest_asyncio.fixture
async def unexposed_puzzle(session):
    with open("test/example/example_map.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    _map = json_data.get("map", None)
    _answers = json_data.get("desc", None)

    map_row = models.Puzzle(puzzle=_map)
    session.add(map_row)
    session.flush()

    insert_data = [
        {"puzzle_id": map_row.id, "word_id": desc["id"], "num": desc["num"]} for desc in _answers
    ]

    session.bulk_insert_mappings(models.PuzzleAnswer, insert_data)
    session.commit()
