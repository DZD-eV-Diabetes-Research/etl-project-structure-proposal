from typing import List, Literal, Generic
from pathlib import Path
from pydantic import BaseModel, Field
import csv
from plisetl.import_model._plis_csv_base import PlisCsvRowBase, PlisCsvBase


class PersonenvariablenCSVRow(PlisCsvRowBase):
    PatientID: str
    Geburtsjahr: int
    Alter_bei_Export: int = Field(alias="Alter bei Export")
    Geschlecht: Literal["männlich", "weiblich", "unbekannt"]
    Site: str
    Register: str
    Erfassungsdatum: str
    RecordLinkage: str
    PSNProben: str


class PersonenvariablenCSV(PlisCsvBase[PersonenvariablenCSVRow]):
    rows: List[PersonenvariablenCSVRow]
