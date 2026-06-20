import os
from dotenv import load_dotenv

# 1. Загружаем переменные окружения из файла .env
load_dotenv()


# 2. Создаем класс Settings для хранения конфигурации
class Settings:
    # 3. Читаем переменные окружения с помощью os.getenv()
    DB_HOST: str = os.getenv("FSTR_DB_HOST", "localhost")
    DB_PORT: str = os.getenv("FSTR_DB_PORT", "5432")
    DB_LOGIN: str = os.getenv("FSTR_DB_LOGIN", "fst_user")
    DB_PASS: str = os.getenv("FSTR_DB_PASS", "password")
    DB_NAME: str = os.getenv("FSTR_DB_NAME", "fst_db")


# 4. Создаем экземпляр класса Settings
settings = Settings()