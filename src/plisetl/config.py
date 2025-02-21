from pydantic import Field
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Literal

env_file_path = os.environ.get("PLIS_ETL_DOT_ENV_FILE", Path(__file__).parent / ".env")


class Config(BaseSettings):
    APP_NAME: str = "PLIS ETL"
    LOG_LEVEL: Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"] = Field(
        default="INFO"
    )
    SQL_DATABASE_URL: str = Field(default="sqlite:///./local.sqlite")
    SQL_DEBUG: bool = Field(
        default=False,
        description="If set to true, the sql engine will print out all sql queries to the log.",
    )
    PSEUDONYMIZATION_SECRET: str = Field(
        description="This is a secret pepper value used to add an additional layer of security to the pseudonymization process, ensuring that site names cannot be deterministically reversed or re-pseudonymized. This value should be kept confidential and consistent across deployments to maintain data integrity while preventing unauthorized re-computation of pseudonyms."
    )
    BITCARE_DIS_EXPORT_CSVS_DIR: str = Field(
        description="The directory that contains all the csv export from the bitcare DIS software"
    )

    class Config:
        env_file = env_file_path
