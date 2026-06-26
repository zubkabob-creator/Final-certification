import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_HOST: str = os.getenv("FSTR_DB_HOST", "localhost")
    DB_PORT: str = os.getenv("FSTR_DB_PORT", "5432")
    DB_LOGIN: str = os.getenv("FSTR_DB_LOGIN", "fst_user")
    DB_PASS: str = os.getenv("FSTR_DB_PASS", "password")
    DB_NAME: str = os.getenv("FSTR_DB_NAME", "fst_db")


settings = Settings()