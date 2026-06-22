import databases, sqlalchemy
from fastapi import FastAPI, HTTPException, status as http_status
from .db import database, metadata, add_pass, get_pass, passes
from .schemas import SubmitDataIn, SubmitDataOut, ErrorResponse, PassOut, PatchResult, PartialSubmitDataIn
from typing import List
from sqlalchemy import cast, Text

app = FastAPI(title="FSTR Mountain Pass API")


@app.on_event("startup")
async def startup():
    """Подключаемся к базе данных и создаем таблицы при запуске."""
    await database.connect()

    # --- Создаем таблицы, если их нет ---
    engine = sqlalchemy.create_engine(str(database.url))
    metadata.create_all(engine)

    print("✅ Успешно подключились к базе данных и создали таблицы!")


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post(
    "/submitData",
    response_model=SubmitDataOut,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },  # <--- ЗАКРЫВАЮЩАЯ СКОРБУКА
)
async def submit_data(request_data: SubmitDataIn):  # <--- НА ТОЙ ЖЕ СТОЛБЦЕ
    try:
        new_id = await add_pass(request_data.dict())
        return SubmitDataOut(id=new_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"status": 500, "message": "Ошибка при выполнении операции"}
        )


@app.get("/submitData/{pass_id}", response_model=PassOut)
async def get_pass_by_id(pass_id: int):
    query = passes.select().where(passes.c.id == pass_id)
    record = await database.fetch_one(query)
    if not record:
        raise HTTPException(status_code=404, detail="Перевал не найден")
    return dict(record)


@app.patch("/submitData/{pass_id}", response_model=PatchResult)
async def patch_pass(pass_id: int, updated_data: PartialSubmitDataIn):
    # 1. Проверка существования
    current_query = passes.select().where(passes.c.id == pass_id)
    current_record = await database.fetch_one(current_query)
    if not current_record:
        return PatchResult(state=0, message="Перевал не найден")

    # 2. Проверка статуса
    if current_record["status"] != "new":
        return PatchResult(state=0, message="Нельзя редактировать запись, находящуюся в обработке")

    # 3. Готовим данные для обновления (только присланные поля)
    allowed_fields = updated_data.model_dump(exclude_unset=True)

    # 4. Исключаем user_info (защита)
    allowed_fields.pop("user_info", None)

    # 5. Используем SQLAlchemy для построения запроса
    # Это безопасный и кросс-базовый способ
    update_query = (
        passes.update()
        .where(passes.c.id == pass_id)
        .values(**allowed_fields)
    )

    # 6. Выполняем
    await database.execute(update_query)

    return PatchResult(state=1)


@app.get("/submitData/", response_model=List[PassOut])
async def get_passes_by_email(user__email: str):
    query = passes.select().where(
        cast(passes.c.user_info['email'], Text) == user__email
    )
    records = await database.fetch_all(query)
    return [dict(rec) for rec in records]


async def submit_data(request_data: SubmitDataIn):
    try:
        new_id = await add_pass(request_data.dict())
        return SubmitDataOut(id=new_id)
    except Exception as e:
        print(f"⚠️ Ошибка при записи в БД: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": 500, "message": "Ошибка при выполнении операции"}
        )