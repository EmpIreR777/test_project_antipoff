import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


env_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env')

load_dotenv(env_file_path, override=True)


class Settings(BaseSettings):

    DATABASE_URL: str
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str
    # POSTGRES_DB: str
    # POSTGRES_HOST: str
    # POSTGRES_PORT: str

    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=env_file_path
    )

    # def get_database_url(self) -> str:
    #     """Возвращает путь к базе данных."""
    #     return (
    #         f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
    #         f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
    #         )


settings = Settings()