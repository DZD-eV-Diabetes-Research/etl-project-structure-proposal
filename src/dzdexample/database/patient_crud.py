from typing import Optional, List
from sqlmodel import select
from dzdexample.database._connection import get_session
from dzdexample.model.patient import Patient

from dzdexample.log import get_logger
from dzdexample.config import Config


class PatientCRUD:
    def get(patient_id: int) -> Optional[Patient]:
        patient = None
        with get_session() as session:
            patient = session.get(Patient, patient_id)
        return patient

    def list_all() -> List[Patient]:
        patients = None
        with get_session() as session:
            patients = session.exec(select(Patient)).all()
        return patients

    def upsert(self, patient: Patient) -> Patient:
        """Update patient or insert if not exists"""
        existing_patient = self.get(patient.id)
        if existing_patient is not None:
            for attr, val in patient.model_dump(exclude_unset=True).items():
                setattr(existing_patient, attr, val)
            with get_session() as session:
                session.add(existing_patient)
                session.commit()
            return existing_patient
        with get_session() as session:
            session.add(patient)
            session.commit()
        return patient
