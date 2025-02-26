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


class CareSiteTransformator:

    def __init__(self, personsvar_csv_data: PersonenvariablenCSV):
        self.personsvariable_csv_data = personsvar_csv_data

    def transform(self) -> List[omop54.CareSite]:
        result: List[omop54.CareSite] = []
        for (
            personsvariable_csv_cell_site
        ) in self.personsvariable_csv_data.get_column_values(
            "Site", distinct_values=True
        ):
            pseudo_id_caresite = self._transform_dis_id_to_omop_id(
                personsvariable_csv_cell_site
            )
            care_site_full_name = self._resolve_caresite_abbreviation(
                personsvariable_csv_cell_site
            )

            result.append(
                omop54.CareSite(
                    care_site_id=pseudo_id_caresite,
                    care_site_name=care_site_full_name,
                    care_site_source_value=personsvariable_csv_cell_site,
                    # location_id=pseudo_id_caresite, # location id makes no sense here. it should be an id of an existing omop54.Location instance not some random str
                )
            )
        return result

    def _resolve_caresite_abbreviation(self, abbreviation: str) -> Dict:
        caresite_mapping = {
            "DDZ": "German Diabetes Center (DDZ)",
            "DIF": "German Institute of Human Nutrition Potsdam-Rehbruecke (DIfE)",
            "DRE": "Paul Langerhans Institute Dresden (PLID)",
            "LEI": "Helmholtz Institute for Metabolic, Adiposity and Vascular Research (HI-MAG)",
            "LMU": "Faculty of Medicine at LMU Munich",
            "TUB": "Institute for Diabetes Research and Metabolic Diseases (IDM)",
            "TUM": "University Hospital rechts der Isar at TUM",
            "UKH": "Heidelberg University Hospital",
        }
        return caresite_mapping.get(abbreviation, "Unknown")

    def _transform_dis_id_to_omop_id(self, dis_id) -> int:
        """OMOP want to an integers with a length of 10 as the id, but we onyl have the short string from the Bitcare DIS system."""
        return (
            int(
                hashlib.sha256((str(dis_id)).encode("utf-8")).hexdigest(),
                base=16,
            )
            % 10**10
        )
