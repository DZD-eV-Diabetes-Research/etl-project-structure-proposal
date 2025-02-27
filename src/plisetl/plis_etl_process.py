from typing import List
from pathlib import Path
from omopmodel.OMOP_5_4_sqlmodels import CareSite, Person
from plisetl.config import Config
from plisetl.transformator.caresite import CareSiteTransformator
from plisetl.transformator.person import PersonTransformator
from plisetl.database.caresite_crud import CaresideCRUD
from plisetl.database.person_crud import PersonCRUD
from plisetl.import_model.Personenvariablen import PersonenvariablenCSV
from plisetl.log import get_logger

log = get_logger()
config = Config()


def run_plis_etl():
    # start with Caresite table
    log.info("Start importing and transforming CareSites from 'Personenvariablen.csv'")
    care_site_omop_data = import_and_transform_care_site(
        csv_file_name="Personenvariablen.csv"
    )

    log.info(
        f"Write OMOP CDM CareSites (Amount: {len(care_site_omop_data)}) into database."
    )
    CaresideCRUD().insert_bulk(care_site_omop_data)

    # continue with Person table
    log.info("Start importing and transforming Persons from 'Personenvariablen.csv'")
    person_omop_data = import_and_transform_person(
        csv_file_name="Personenvariablen.csv"
    )

    log.info(f"Write OMOP CDM Person (Amount: {len(person_omop_data)}) into database.")
    PersonCRUD().insert_bulk(person_omop_data)


def import_and_transform_care_site(csv_file_name: str) -> List[CareSite]:
    csv_file_path = Path(config.BITCARE_DIS_EXPORT_CSVS_DIR, csv_file_name)
    csv_data = PersonenvariablenCSV.from_csv_file(csv_file_path)
    transformer = CareSiteTransformator(csv_data)
    return transformer.transform()


def import_and_transform_person(csv_file_name: str) -> List[Person]:
    csv_file_path = Path(config.BITCARE_DIS_EXPORT_CSVS_DIR, csv_file_name)
    csv_data = PersonenvariablenCSV.from_csv_file(csv_file_path)
    transformer = PersonTransformator(csv_data)
    return transformer.transform()
