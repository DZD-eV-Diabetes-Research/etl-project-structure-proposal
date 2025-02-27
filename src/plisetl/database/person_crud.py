from typing import Optional, List
from sqlmodel import select, delete
from sqlalchemy import exc
from omopmodel.OMOP_5_4_sqlmodels import Person
from plisetl.database._connection import get_session


from plisetl.log import get_logger
from plisetl.config import Config

log = get_logger()


class PersonCRUD:
    def get(person_id: int) -> Optional[Person]:
        """Read a person from the Database by its person_id"""
        person = None
        with get_session() as session:
            person = session.get(Person, person_id)
        return person

    def list_all() -> List[Person]:
        """Read all Persons from the database"""
        persons = None
        with get_session() as session:
            persons = session.exec(select(Person)).all()
        return persons

    def upsert(self, person: Person) -> Person:
        """Update persone or insert if not exists"""
        existing_person = self.get(person.person_id)
        if existing_person is not None:
            for attr, val in person.model_dump(exclude_unset=True).items():
                setattr(existing_person, attr, val)
            with get_session() as session:
                session.add(existing_person)
                session.commit()
            return existing_person
        with get_session() as session:
            session.add(person)
            session.commit()
        return person

    def insert_bulk(self, persons: List[Person]) -> List[Person]:
        """Insert a list of persons at once. This will be more perfomant compared `upsert` but does not exists check."""
        log.debug(f"Insert {len(persons)} Person rows")
        with get_session() as session:
            session.add_all(persons)
            session.commit()
        return persons

    def truncate_table(self, table_not_exists_ok=False):
        """Delete all rows from table Person."""
        log.warning(f"Truncate table Person...")
        with get_session() as session:
            statement = delete(Person)
            try:
                result = session.exec(statement)
                session.commit()
                log.warning(f"...deleted {result.rowcount} Person rows")
            except (exc.NoSuchTableError, exc.OperationalError) as e:
                if (
                    isinstance(e, exc.NoSuchTableError)
                    or (
                        isinstance(e, exc.OperationalError)
                        and "no such table" in e._message()
                    )
                ) and table_not_exists_ok:
                    log.info(f"...nothing to truncate. Table `Person` does not exists.")
                else:
                    raise e
