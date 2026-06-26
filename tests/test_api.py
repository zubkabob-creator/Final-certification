import pytest, pytest_asyncio, json
from fastapi.testclient import TestClient
from app.main import app
from app.db import database, passes
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import sqlalchemy

load_dotenv("../.env.testing")

DATABASE_URL = f"postgresql://" \
               f"{os.getenv('FSTR_DB_LOGIN')}:{os.getenv('FSTR_DB_PASS')}" \
               f"@{os.getenv('FSTR_DB_HOST')}:{os.getenv('FSTR_DB_PORT')}" \
               f"/{os.getenv('FSTR_DB_NAME')}"

@pytest_asyncio.fixture
async def client():
    client = TestClient(app)
    async with app.router.lifespan_context(app):
        yield client

@pytest.mark.asyncio
async def test_full_cycle(client):
    payload = {
        "name": "Integration Test",
        "latitude": 47.123,
        "longitude": 78.456,
        "altitude_m": 3500,
        "photos": ["https://example.com/integration.jpg"],
        "user_info": {
            "name": "Иван Петрович",
            "email": "integration@test.ru",
            "phone": "79991234567"
        },
    }

    resp_create = client.post("/submitData", json=payload)
    assert resp_create.status_code == 200
    new_id = resp_create.json()["id"]

    resp_read = client.get(f"/submitData/{new_id}")
    assert resp_read.status_code == 200
    retrieved = resp_read.json()
    assert retrieved["name"] == "Integration Test"

    resp_update = client.patch(f"/submitData/{new_id}", json={"name": "Updated Integration"})
    assert resp_update.json()["state"] == 1

    await database.execute(
        passes.update().where(passes.c.id == new_id).values(status="pending")
    )

    resp_protect = client.patch(f"/submitData/{new_id}", json={"name": "Hack Attempt"})
    assert resp_protect.json()["state"] == 0

    resp_filter = client.get("/submitData/?user__email=integration@test.ru")
    assert resp_filter.status_code == 200
    filtered = resp_filter.json()
    assert len(filtered) == 1
    assert filtered[0]["id"] == new_id