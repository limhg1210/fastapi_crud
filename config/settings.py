from dotenv import load_dotenv, find_dotenv

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int


def get_settings(env_name: str = "default"):
    env_file_name = {
        "default": ".env",
        "test": ".env.test",
    }[env_name]

    load_dotenv(env_file_name, encoding="utf-8")

    return Settings()
