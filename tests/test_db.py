import pytest
import pytest_asyncio
from app.db import database, add_pass, get_pass, SyncSession
from app.schemas import SubmitDataIn
from dotenv import load_dotenv
from app.config import Settings
from sqlalchemy import text
import json

load_dotenv("../.env")
settings = Settings()

@pytest.fixture(autouse=True)
def session():
    sess = SyncSession()
    yield sess
    sess.close()

def test_add_and_get_pass(session):
    data_in = {
        "name": "Test Mountain",
        "latitude": 47.123,
        "longitude": 78.456,
        "altitude_m": 3500,
        "photos": json.dumps(["https://example.com/photo3.jpg"]),
        "user_info": json.dumps({"name": "Alexey", "email": "alexey@test.ru", "phone": "79991234567"}),
    }

    session.execute(
        text(
            "INSERT INTO passes (name, latitude, longitude, altitude_m, photos, user_info, status) "
            "VALUES (:name, :latitude, :longitude, :altitude_m, :photos, :user_info, 'new') RETURNING id"
        ),
        data_in
    )
    new_id = session.scalar(text("SELECT LASTVAL()"))

    retrieved = session.execute(
        text("SELECT * FROM passes WHERE id = :id"),
        {"id": new_id}
    ).fetchone()

    assert retrieved.name == "Test Mountain"
    assert retrieved.user_info["email"] == "alexey@test.ru"
    assert retrieved.photos[0] == "https://example.com/photo3.jpg"


@pytest_asyncio.fixture
async def db_setup():
    await database.connect()
    yield
    await database.disconnect()

@pytest.mark.asyncio
async def test_get_existing_pass(db_setup):
    data_in = {
        "name": "Test Mountain",
        "latitude": 47.123,
        "longitude": 78.456,
        "altitude_m": 3500,
        "photos": ["https://example.com/1.jpg"],
        "user_info": {"name": "Alexey", "email": "alexey@test.ru", "phone": "79991234567"}
    }
    new_id = await add_pass(data_in)

    retrieved = await get_pass(new_id)
    assert retrieved["id"] == new_id
    assert retrieved["name"] == "Test Mountain"

@pytest.mark.asyncio
async def test_get_nonexistent_pass(db_setup):
    nonexistent = await get_pass(-1)
    assert nonexistent is None