from pydantic_settings import BaseSettings, SettingsConfigDict
import os

#Класс хранилище переменных для подключения к базе данных
#Class storing variables for connecting to a database
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()