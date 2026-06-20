import json
import databases
import sqlalchemy
from sqlalchemy.sql import func

# --- 1. Подключение к БД ---
from .config import settings

DATABASE_URL = f"postgresql://{settings.DB_LOGIN}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# --- 2. Определение структуры таблицы (Модели) ---
passes = sqlalchemy.Table(
    "passes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("latitude", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("longitude", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("altitude_m", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("photos", sqlalchemy.JSON, nullable=False),
    sqlalchemy.Column("user_info", sqlalchemy.JSON, nullable=False),
    sqlalchemy.Column(
        "status",
        sqlalchemy.Enum('new', 'pending', 'accepted', 'rejected', name='pass_status'),
        nullable=False,
        server_default='new'
    ),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime(timezone=True), server_default=func.now()),
)

# --- 3. Методы для работы с данными (CRUD) ---
async def add_pass(data: dict) -> int:
    query = passes.insert().values(
        name=data["name"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        altitude_m=data["altitude_m"],
        photos=data["photos"],
        user_info=data["user_info"],
        status='new'
    )
    last_record_id = await database.execute(query)
    return last_record_id

async def get_pass(pass_id: int):
    query = passes.select().where(passes.c.id == pass_id)
    return await database.fetch_one(query)