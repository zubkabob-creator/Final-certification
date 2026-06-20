import databases, sqlalchemy
from fastapi import FastAPI, HTTPException, status as http_status

from .db import database, metadata, add_pass, get_pass
from .schemas import SubmitDataIn, SubmitDataOut, ErrorResponse

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
    },
)
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