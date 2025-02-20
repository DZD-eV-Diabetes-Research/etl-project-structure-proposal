from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Literal

class Config(BaseSettings):
    APP_NAME: str = "DZDMedLog"
    LOG_LEVEL: Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"] = Field(
        default="INFO"
    )
    SQL_DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./local.sqlite")
    DEBUG_SQL: bool = Field(
        default=False,
        description="If set to true, the sql engine will print out all sql queries to the log.",
    )