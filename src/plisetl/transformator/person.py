from typing import Optional, Dict, List
import hashlib
from sqlmodel import SQLModel, Field
from pydantic import Field, BaseModel
from omopmodel import OMOP_5_4_sqlmodels as omop54
from plisetl.log import get_logger
from plisetl.config import Config
from plisetl.import_model.Personenvariablen import (
    PersonenvariablenCSVRow,
    PersonenvariablenCSV,
)

from plisetl.utils import pseudonymize_value_to_int, pseudonymize_value_to_str


class PersonTransformator:

    def __init__(self, personsvar_csv_data: PersonenvariablenCSV):
        self.personsvariable_csv_data = personsvar_csv_data

    def transform(self) -> List[omop54.Person]:
        result: List[omop54.Person] = []
        for (
            personsvariable_csv_cell_patient
        ) in self.personsvariable_csv_data.get_column_values(
            "PatientID", distinct_values=True
        ):
            pseudo_id_person = self.pseudonymize_value_to_int(
                personsvariable_csv_cell_patient
            )

        for (
            personsvariable_csv_cell_geschlecht
        ) in self.personsvariable_csv_data.get_column_values("Geschlecht"):
            if self.Geschlecht == "weiblich":
                gender_concept_id = 8532

            elif self.Geschlecht == "männlich":
                gender_concept_id = 8507

            else:
                gender_concept_id = 0

            pseudo_id_person = self.pseudonymize_value_to_int(
                personsvariable_csv_cell_geschlecht
            )

            result.append(
                omop54.Person(
                    person_id=pseudo_id_person,
                    year_of_birth=self.Geburtsjahr,
                    gender_concept_id=gender_concept_id,
                    race_concept_id=0,
                    ethnicity_concept_id=0,
                    # care_site_id=pseudo_id_caresite,  # careside and location id makes no sense here. it should be an id of an existing omop54.Location instance not some random str
                )
            )
        return result
