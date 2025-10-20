from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
load_dotenv(dotenv_path)

#Класс хранилище переменных для подключения к базе данных
#Class storing variables for connecting to a database
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    model_config = SettingsConfigDict(
        env_file=dotenv_path
    )


settings = Settings()