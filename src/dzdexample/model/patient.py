from typing import Optional
from sqlmodel import SQLModel, Field
from dzdexample.log import get_logger
from dzdexample.config import Config

# This is just an exemplary demo class and should be replaced/removed


class Patient(SQLModel):
    id: int = Field(primary_key=True, description="The id of the Patient")
    name: str = Field(description="The name of the Patient")
    email: Optional[str] = Field(
        description="If the patient supplied an email it is stored here", default=None
    )
