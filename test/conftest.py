import pytest_asyncio
import pandas as pd

from httpx import AsyncClient
from sqlalchemy import text

from app import main, models
from app.config import settings
from app.database import engine, get_db


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
