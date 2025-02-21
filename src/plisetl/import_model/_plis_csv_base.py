from typing import List, Literal, TypeVar, Type, Generic, get_args
from pathlib import Path
from pydantic import BaseModel, Field
import csv
from plisetl.log import get_logger

log = get_logger()

# Define a generic type variable for row classes
GenericCsvRowType = TypeVar("T", bound="PlisCsvRowBase")


class PlisCsvRowBase(BaseModel):
    parent_csv: "PlisCsvBase"
    row_num: int

    @classmethod
    def from_raw_csv_row(
        cls: Type[GenericCsvRowType],
        row: List[str],
        parent_csv: "PlisCsvBase",
        row_num: int,
    ):
        object_values = {"parent_csv": parent_csv, "row_num": row_num}
        for field_name, field_info in cls.model_fields.items():
            if field_name in ["parent_csv", "row_num"]:
                # filter metadata fields
                continue
            csv_column_name = field_info.alias or field_name

            cell_value = row[parent_csv.headers.index(csv_column_name)]
            object_values[csv_column_name] = cell_value
        try:
            return cls.model_validate(object_values)
        except:
            log.error(
                f"Failed to parse row no {row_num} in file {parent_csv.source_csv_file_path.resolve()}. Row Content:\n{row}"
            )
            raise

    def get_column_value(self, column_name: str):
        if column_name not in self.parent_csv.headers:
            # check model attrs aliases for column name
            column_name_alias = None
            for field_name, field_info in self.model_fields.items():
                if field_info.alias == column_name:
                    column_name_alias = field_info.alias

            if column_name_alias is None:
                raise ValueError(
                    f"Column '{column_name}' does not exist in {self.parent_csv.__name__}"
                )
            column_name = column_name_alias
        return getattr(self, column_name)


class PlisCsvBase(BaseModel, Generic[GenericCsvRowType]):
    rows: List[GenericCsvRowType]
    headers: List[str]
    source_csv_file_path: Path

    @classmethod
    def from_csv_file(
        cls: Type["PlisCsvBase[GenericCsvRowType]"], source_csv_file_path: Path
    ) -> Type[GenericCsvRowType]:
        csv_object = cls(rows=[], headers=[], source_csv_file_path=source_csv_file_path)
        with open(source_csv_file_path, encoding="utf-8") as csv_file:

            csv_reader = csv.reader(csv_file, delimiter=";")
            csv_object.headers = next(
                csv_reader
            )  # step into first line (column headers) of csv

            # continue with data rows
            for row_number, row in enumerate(csv_reader):
                csv_object.rows.append(
                    cls._get_row_type().from_raw_csv_row(
                        row, parent_csv=csv_object, row_num=row_number + 1
                    )
                )
        return csv_object

    def get_column_values(
        self, column_name, distinct_values: bool = False
    ) -> List[str]:
        if distinct_values:
            return list(set(row.get_column_value(column_name) for row in self.rows))
        return list(row.get_column_value(column_name) for row in self.rows)

    @classmethod
    def _get_row_type(cls) -> Type[GenericCsvRowType]:
        """Automatically extract the row type from the generic subclass declaration"""
        rows_field_info = next(
            field_info
            for field_name, field_info in cls.model_fields.items()
            if field_name == "rows"
        )
        row_type = get_args(rows_field_info.annotation)[0]
        return row_type
