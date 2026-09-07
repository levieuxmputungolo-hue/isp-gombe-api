from pydantic import BaseModel
from typing import Optional


class SearchByMatricule(BaseModel):
    matricule: str
    promotion: str = ""
    annee_academique: str = ""


class SearchByName(BaseModel):
    full_name: str
    promotion: str
    level: str
    option: str = ""
    section: str = ""


class ResultOut(BaseModel):
    code_ue: str
    intitule_ue: str
    bci: str
    categorie: str
    credits: int
    note: float
    note_ponderee: float
    session: str

    class Config:
        from_attributes = True


class BulletinSummary(BaseModel):
    total_credits: int
    total_pondere: float
    moyenne: float
    moyenne_a: float
    moyenne_b: float
    decision: str
    mention: str
    credits_capitalises: int


class StudentOut(BaseModel):
    matricule: str
    full_name: str
    promotion: str
    level: str
    option: str
    section: str
    annee_academique: str
    university: Optional[str] = None
    results: list[ResultOut] = []
    bulletin: Optional[BulletinSummary] = None

    class Config:
        from_attributes = True


class StudentListItem(BaseModel):
    matricule: str
    full_name: str
    promotion: str
    level: str
    option: str
    annee_academique: str


class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None


class ImportResult(BaseModel):
    imported: int
    skipped: int
    errors: list[str] = []


class ImportRow(BaseModel):
    matricule: str
    nom_complet: str
    code_ue: str
    intitule_ue: str
    bci: str
    categorie: str
    credits: int
    note: float
    session: str = "Normal"
    annee_academique: str
    promotion: str
    option: str
    section: str
