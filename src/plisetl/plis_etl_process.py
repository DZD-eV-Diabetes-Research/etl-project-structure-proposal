from typing import List
from pathlib import Path
from omopmodel.OMOP_5_4_sqlmodels import CareSite
from plisetl.config import Config
from plisetl.transformator.caresite import CareSiteTransformator
from plisetl.database.caresite_crud import CaresideCRUD
from plisetl.import_model.Personenvariablen import PersonenvariablenCSV
from plisetl.log import get_logger

log = get_logger()
config = Config()


def run_plis_etl():
    log.info("Start importing and transforming CareSites from 'Personenvariablen.csv'")
    care_site_omop_data = import_and_transform_care_site(
        csv_file_name="Personenvariablen.csv"
    )

    log.info(
        f"Write OMOP CDM CareSites (Amount: {len(care_site_omop_data)}) into database."
    )
    CaresideCRUD().insert_bulk(care_site_omop_data)


def import_and_transform_care_site(csv_file_name: str) -> List[CareSite]:
    csv_file_path = Path(config.BITCARE_DIS_EXPORT_CSVS_DIR, csv_file_name)
    csv_data = PersonenvariablenCSV.from_csv_file(csv_file_path)
    transformer = CareSiteTransformator(csv_data)
    return transformer.transform()
