# Models in

This directory contains classes that represent the data structure of all data that will ingested in the ETL process

As a the base class for every dataclass we use either [SQLModel](https://sqlmodel.tiangolo.com/).sqlmodel if we need to store the data in a SQLDatabase
or we use Pydantic for datahandling without the need to store it into a SQLDatabase
