from typing import Optional, List
from sqlmodel import select, delete
from omopmodel.OMOP_5_4_sqlmodels import CareSite
from plisetl.database._connection import get_session


from plisetl.log import get_logger
from plisetl.config import Config

log = get_logger()


class CaresideCRUD:
    def get(caresite_id: int) -> Optional[CareSite]:
        caresite = None
        with get_session() as session:
            caresite = session.get(CareSite, caresite_id)
        return caresite

    def list_all() -> List[CareSite]:
        caresites = None
        with get_session() as session:
            caresites = session.exec(select(CareSite)).all()
        return caresites

    def upsert(self, caresite: CareSite) -> CareSite:
        """Update caresite or insert if not exists"""
        existing_caresite = self.get(caresite.care_site_id)
        if existing_caresite is not None:
            for attr, val in caresite.model_dump(exclude_unset=True).items():
                setattr(existing_caresite, attr, val)
            with get_session() as session:
                session.add(existing_caresite)
                session.commit()
            return existing_caresite
        with get_session() as session:
            session.add(caresite)
            session.commit()
        return caresite

    def insert_bulk(self, caresites: List[CareSite]) -> List[CareSite]:
        log.debug(f"Insert {len(caresites)} CareSite rows")
        with get_session() as session:
            session.add_all(caresites)
            session.commit()
        return caresites

    def truncate_table(self):
        log.warning(f"Truncate table CareSite...")
        with get_session() as session:
            statement = delete(CareSite)
            result = session.exec(statement)
            session.commit()
            log.warning(f"...deleted {result.rowcount} CareSites rows")
