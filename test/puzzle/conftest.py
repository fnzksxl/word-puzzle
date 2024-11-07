import pytest_asyncio
import json

from app import models


@pytest_asyncio.fixture
async def four_puzzles(session):
    with open("test/example/example_map.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    _map = json_data.get("map", None)
    across = json_data.get("across", None)
    down = json_data.get("down", None)

    for _ in range(4):
        map_row = models.Puzzle(puzzle=_map, is_exposed=True)
        session.add(map_row)
        session.flush()

        across_data = [
            {
                "puzzle_id": map_row.id,
                "start_x": desc["startpoint"][0],
                "start_y": desc["startpoint"][1],
                "dir": "across",
                "word_id": 1,
                "num": desc["num"],
            }
            for desc in across
        ]
        down_data = [
            {
                "puzzle_id": map_row.id,
                "start_x": desc["startpoint"][0],
                "start_y": desc["startpoint"][1],
                "dir": "down",
                "word_id": 1,
                "num": desc["num"],
            }
            for desc in down
        ]

        session.bulk_insert_mappings(models.PuzzleAnswer, across_data + down_data)
        session.commit()

    return {"id": map_row.id, "name": map_row.name}


@pytest_asyncio.fixture
async def unexposed_puzzle(session):
    with open("test/example/example_map.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    _map = json_data.get("map", None)
    across = json_data.get("across", None)
    down = json_data.get("down", None)

    map_row = models.Puzzle(puzzle=_map)
    session.add(map_row)
    session.flush()

    across_data = [
        {
            "puzzle_id": map_row.id,
            "start_x": desc["startpoint"][0],
            "start_y": desc["startpoint"][1],
            "dir": "across",
            "word_id": 1,
            "num": desc["num"],
        }
        for desc in across
    ]
    down_data = [
        {
            "puzzle_id": map_row.id,
            "start_x": desc["startpoint"][0],
            "start_y": desc["startpoint"][1],
            "dir": "down",
            "word_id": 1,
            "num": desc["num"],
        }
        for desc in down
    ]

    session.bulk_insert_mappings(models.PuzzleAnswer, across_data + down_data)
    session.commit()

    return {"id": map_row.id, "name": map_row.name}
