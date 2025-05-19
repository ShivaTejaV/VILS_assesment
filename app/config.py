from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",        # ignore other env vars
    )

    db_url: AnyUrl = Field(..., alias="DB_URL")

settings = Settings()  # type: ignore

