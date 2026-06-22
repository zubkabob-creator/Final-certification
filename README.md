<img width="1438" height="1125" alt="swagger-ui" src="https://github.com/user-attachments/assets/9921b180-dc95-4aa4-b648-5cfd4e69e894" />
<img width="3439" height="253" alt="openapi-spec" src="https://github.com/user-attachments/assets/efae2166-39c3-4b4f-9161-8c7b40f089b2" />
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
