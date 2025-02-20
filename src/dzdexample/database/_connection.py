from typing import List
from sqlmodel import SQLModel, Field, Session, create_engine, select


from dzdexample.config import Config
from dzdexample.log import get_logger

config = Config()
log = get_logger()


db_engine = create_engine(config.SQL_DATABASE_URL, echo=config.SQL_DEBUG)


# Create the database tables (only needed initially)
def init_db():
    from dzdexample.model.patient import Patient

    SQLModel.metadata.create_all(db_engine)


def get_session():
    return Session(db_engine)
