import math
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db import get_db
from app.models import Student, Result, University
from app.schemas import (
    SearchByMatricule, SearchByName, StudentOut, ResultOut,
    BulletinSummary, ImportRow, ImportResult, StudentListItem,
)

router = APIRouter(prefix="/api/results", tags=["Results"])

GRADE_MAP = [
    (16, 20, "A", "TRES BIEN"),
    (14, 16, "B", "BIEN"),
    (12, 14, "C", "ASSEZ BIEN"),
    (10, 12, "D", "PASSABLE"),
    (0, 10, "F", "INSUFFISANT"),
]


def compute_grade(score: float) -> str:
    for lo, hi, g, _ in GRADE_MAP:
        if lo <= score < hi or (hi == 20 and score == 20):
            return g
    return "F"


def compute_mention(moy: float) -> str:
    if moy >= 16:
        return "TRES BIEN"
    elif moy >= 14:
        return "BIEN"
    elif moy >= 12:
        return "ASSEZ BIEN"
    elif moy >= 10:
        return "PASSABLE"
    return "—"


def compute_bulletin(results: list) -> BulletinSummary:
    total_credits = 0
    total_pondere = 0.0
    total_credits_a = 0
    total_pondere_a = 0.0
    total_credits_b = 0
    total_pondere_b = 0.0

    for r in results:
        pond = r.note * r.credits
        total_credits += r.credits
        total_pondere += pond
        if r.categorie == "A":
            total_credits_a += r.credits
            total_pondere_a += pond
        else:
            total_credits_b += r.credits
            total_pondere_b += pond

    if total_credits == 0:
        return BulletinSummary(
            total_credits=0, total_pondere=0, moyenne=0,
            moyenne_a=0, moyenne_b=0, decision="AJOURNE",
            mention="—", credits_capitalises=0,
        )

    moyenne = total_pondere / total_credits
    moyenne_a = total_pondere_a / total_credits_a if total_credits_a > 0 else 0.0
    moyenne_b = total_pondere_b / total_credits_b if total_credits_b > 0 else 0.0
    decision = "ADMIS" if moyenne >= 10 else "AJOURNE"
    mention = compute_mention(moyenne) if moyenne >= 10 else "—"
    credits_capitalises = total_credits if moyenne >= 10 else sum(
        r.credits for r in results if r.note >= 10
    )

    return BulletinSummary(
        total_credits=total_credits,
        total_pondere=round(total_pondere, 2),
        moyenne=round(moyenne, 2),
        moyenne_a=round(moyenne_a, 2),
        moyenne_b=round(moyenne_b, 2),
        decision=decision,
        mention=mention,
        credits_capitalises=credits_capitalises,
    )


def build_student_out(student: Student, db: Session) -> StudentOut:
    university_name = None
    if student.university_id:
        uni = db.query(University).filter(University.id == student.university_id).first()
        if uni:
            university_name = uni.name

    results_out = []
    for r in student.results:
        results_out.append(ResultOut(
            code_ue=r.code_ue,
            intitule_ue=r.intitule_ue,
            bci=r.bci,
            categorie=r.categorie,
            credits=r.credits,
            note=r.note,
            note_ponderee=r.note_ponderee,
            session=r.session,
        ))

    bulletin = compute_bulletin(student.results)

    return StudentOut(
        matricule=student.matricule,
        full_name=student.full_name,
        promotion=student.promotion,
        level=student.level,
        option=student.option,
        section=student.section,
        annee_academique=student.annee_academique,
        university=university_name,
        results=results_out,
        bulletin=bulletin,
    )


@router.post("/search", response_model=StudentOut)
def search_by_matricule(req: SearchByMatricule, db: Session = Depends(get_db)):
    filters = [Student.matricule == req.matricule]
    if req.promotion:
        filters.append(Student.promotion == req.promotion)
    if req.annee_academique:
        filters.append(Student.annee_academique == req.annee_academique)

    student = db.query(Student).filter(and_(*filters)).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aucun etudiant trouve avec ce matricule.")

    return build_student_out(student, db)


@router.post("/search-by-name", response_model=StudentOut)
def search_by_name(req: SearchByName, db: Session = Depends(get_db)):
    filters = [
        Student.full_name.ilike(f"%{req.full_name}%"),
        Student.promotion == req.promotion,
        Student.level == req.level,
    ]
    if req.option:
        filters.append(Student.option == req.option)
    if req.section:
        filters.append(Student.section == req.section)

    student = db.query(Student).filter(and_(*filters)).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aucun etudiant trouve.")

    return build_student_out(student, db)


@router.get("/students/{matricule}", response_model=list[StudentListItem])
def list_student_entries(matricule: str, db: Session = Depends(get_db)):
    students = db.query(Student).filter(Student.matricule == matricule).all()
    return [
        StudentListItem(
            matricule=s.matricule,
            full_name=s.full_name,
            promotion=s.promotion,
            level=s.level,
            option=s.option,
            annee_academique=s.annee_academique,
        )
        for s in students
    ]


@router.get("/promotions")
def list_promotions(db: Session = Depends(get_db)):
    rows = db.query(Student.promotion).distinct().all()
    db_vals = sorted([r[0] for r in rows if r[0]])
    defaults = ["2024-2025", "2023-2024", "2022-2023"]
    return sorted(list(dict.fromkeys(defaults + db_vals)))


@router.get("/levels")
def list_levels(db: Session = Depends(get_db)):
    rows = db.query(Student.level).distinct().all()
    db_vals = sorted([r[0] for r in rows if r[0]])
    defaults = ["L1", "L2", "L3", "M1", "M2"]
    return sorted(list(dict.fromkeys(defaults + db_vals)))


@router.get("/options")
def list_options(db: Session = Depends(get_db)):
    rows = db.query(Student.option).distinct().all()
    db_vals = sorted([r[0] for r in rows if r[0]])
    defaults = [
        "Informatique de Gestion", "Gestion des entreprises",
        "Mathematiques", "Mathematiques - Informatique",
        "Physique - Chimie", "Sciences commerciales & administratives",
        "Hotellerie & restauration", "Accueil & tourisme",
    ]
    return sorted(list(dict.fromkeys(defaults + db_vals)))


@router.get("/sections")
def list_sections(db: Session = Depends(get_db)):
    rows = db.query(Student.section).distinct().all()
    db_vals = sorted([r[0] for r in rows if r[0]])
    defaults = [
        "Lettres & Sciences Humaines", "Sciences Exactes",
        "Sciences Commerciales & Informatique",
        "Sciences & Techniques d'Accueil", "Section Soir",
    ]
    return sorted(list(dict.fromkeys(defaults + db_vals)))


@router.post("/import-excel", response_model=ImportResult)
def import_excel(rows: list[ImportRow], db: Session = Depends(get_db)):
    imported = 0
    skipped = 0
    errors = []

    for row in rows:
        try:
            if not row.matricule or not row.code_ue:
                skipped += 1
                continue

            note_ponderee = row.note * row.credits

            student = db.query(Student).filter(
                Student.matricule == row.matricule,
                Student.promotion == row.promotion,
                Student.annee_academique == row.annee_academique,
            ).first()

            if not student:
                student = Student(
                    matricule=row.matricule,
                    full_name=row.nom_complet,
                    promotion=row.promotion,
                    level=row.promotion,
                    option=row.option,
                    section=row.section,
                    annee_academique=row.annee_academique,
                )
                db.add(student)
                db.flush()

            existing = db.query(Result).filter(
                Result.student_id == student.id,
                Result.code_ue == row.code_ue,
                Result.bci == row.bci,
                Result.session == row.session,
            ).first()

            if existing:
                existing.note = row.note
                existing.note_ponderee = note_ponderee
                existing.categorie = row.categorie.upper()
            else:
                result = Result(
                    student_id=student.id,
                    code_ue=row.code_ue,
                    intitule_ue=row.intitule_ue,
                    bci=row.bci,
                    categorie=row.categorie.upper(),
                    credits=row.credits,
                    note=row.note,
                    session=row.session,
                    note_ponderee=note_ponderee,
                )
                db.add(result)

            imported += 1
        except Exception as e:
            errors.append(f"Ligne {row.matricule}: {str(e)}")

    db.commit()
    return ImportResult(imported=imported, skipped=skipped, errors=errors)


@router.get("/universities")
def list_universities(db: Session = Depends(get_db)):
    return [{"id": u.id, "name": u.name, "logo_url": u.logo_url} for u in db.query(University).all()]
