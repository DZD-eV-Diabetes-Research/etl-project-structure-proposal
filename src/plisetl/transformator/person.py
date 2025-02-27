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
        for personsvariable_csv_row_patient in self.personsvariable_csv_data.rows:
            pseudo_id_person = pseudonymize_value_to_int(
                personsvariable_csv_row_patient.PatientID
            )

            year_of_birth = personsvariable_csv_row_patient.Geburtsjahr

            gender_concept_id = 0
            if personsvariable_csv_row_patient.Geschlecht == "weiblich":
                gender_concept_id = 8532

            elif personsvariable_csv_row_patient.Geschlecht == "männlich":
                gender_concept_id = 8507

            care_site_id = pseudonymize_value_to_int(
                personsvariable_csv_row_patient.Site, unsalted=True
            )
            result.append(
                omop54.Person(
                    person_id=pseudo_id_person,
                    year_of_birth=year_of_birth,
                    gender_concept_id=gender_concept_id,
                    race_concept_id=0,
                    ethnicity_concept_id=0,
                    care_site_id=care_site_id,
                )
            )

        return result
