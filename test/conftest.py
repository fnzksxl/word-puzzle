import bcrypt
import json
import pytest_asyncio
import pandas as pd

from httpx import AsyncClient
from sqlalchemy import text

from app import main, models
from app.config import settings
from app.database import engine, get_db
from app.api.v1.auth.jwt import JWTService


@pytest_asyncio.fixture(scope="session")
def app():
    if not settings.TESTING:
        raise SystemError("Testing Environment setting must be 'TRUE'")

    return main.app


@pytest_asyncio.fixture
async def session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


@pytest_asyncio.fixture(scope="session")
async def inserted_wordinfo_into_db(app):
    with engine.connect() as connection:
        result = connection.execute(text("SELECT COUNT(*) FROM wordinfo"))
        row_count = result.scalar()

        if row_count > 494047:
            connection.execute(text("DELETE FROM wordinfo"))
            connection.execute(text("ALTER TABLE wordinfo AUTO_INCREMENT = 1"))
        if row_count == 0:
            df = pd.read_csv("test/example/wordinfo_backup.csv")
            df.to_sql("wordinfo", con=engine, index=False, if_exists="append")


@pytest_asyncio.fixture
async def client(app, inserted_wordinfo_into_db):
    async with AsyncClient(app=app, base_url="http://test/api/v1") as ac:
        tables_to_drop = [
            table for table in models.Base.metadata.sorted_tables if table.name != "wordinfo"
        ]

        models.Base.metadata.drop_all(bind=engine, tables=tables_to_drop)
        models.Base.metadata.create_all(bind=engine)
        yield ac


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
    refresh_token = jwt_service.create_refresh_token(user_dict)

    return {"access": access_token, "refresh": refresh_token}


@pytest_asyncio.fixture
async def puzzle(session):
    with open("test/example/example_map.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    _map = json_data.get("map", None)
    across = json_data.get("across", None)
    down = json_data.get("down", None)

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
