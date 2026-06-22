# FSTR Mountain Pass API

REST API for managing mountain passes.

## Установка

1.  Создайте виртуальное окружение:
    ```bash
    python -m venv venv
    ```
2.  Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
3.  Заполните `.env` (скопируйте из `.env.example`).
4.  Запустите сервер:
    ```bash
    uvicorn app.main:app --reload
    ```

    ## Документация

### Endpoints

| Метод | Путь | Описание |
|-------|------|----------|
| POST  | /submitData | Добавить перевал |
| GET   | /submitData/{id} | Получить по ID |
| PATCH | /submitData/{id} | Редактировать (если статус "new") |
| GET   | /submitData/?user__email= | Список по email |

### Примеры использования

#### Создание перевала

curl -X 'POST' \
  'http://127.0.0.1:8000/submitData' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Test Mountain",
  "latitude": 47.123,
  "longitude": 78.456,
  "altitude_m": 3500,
  "photos": ["https://example.com/photo3.jpg"],
  "user_info": {
    "name": "Alexey",
    "email": "alexey@test.ru",
    "phone": "79991234567"
  }
}'

#### Получение по ID

curl -X 'GET' \
  'http://127.0.0.1:8000/submitData/3' \
  -H 'accept: application/json'

#### Редактирование

curl -X 'PATCH' \
  'http://127.0.0.1:8000/submitData/3' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Test Mountain",
  "latitude": 47.123,
  "longitude": 78.456,
  "altitude_m": 3500,
  "photos": ["https://example.com/photo3.jpg"],
  "user_info": {
    "name": "Alexey",
    "email": "alexey@test.ru",
    "phone": "79991234567"
  }
}'

№№№№ Нахождение путей по email

curl -X 'GET' \
  'http://127.0.0.1:8000/submitData/?user__email=alexey%40test.ru' \
  -H 'accept: application/json'
