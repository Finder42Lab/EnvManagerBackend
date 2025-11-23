from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_HOST: str
    DB_PASSWORD: str
    DB_TABLE: str
    DB_USER: str

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_TABLE}"


settings = Config()
