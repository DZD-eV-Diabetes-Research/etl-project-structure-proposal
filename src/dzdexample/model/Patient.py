from typing import Optional
from sqlmodel import SQLModel, Field

# This is just an exemplary demo class and should be replaced/removed


class Patient(SQLModel):
    name: str = Field(description="The name of the Patient")
    email: Optional[str] = Field(description="If the patient supplied an email it is stored here", default=None)
