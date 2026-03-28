from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    algorithm: str = "HS256"
    secret_key: str

    class Config:
        env_file = ".env"

settings = Settings()