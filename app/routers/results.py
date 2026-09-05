from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db import get_db
from app.models import Student, Result, University
from app.schemas import SearchRequest, StudentOut, ResultOut

router = APIRouter(prefix="/api/results", tags=["Results"])


@router.post("/search", response_model=StudentOut)
def search_results(req: SearchRequest, db: Session = Depends(get_db)):
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
        raise HTTPException(
            status_code=404,
            detail="Aucun résultat trouvé pour ces informations. Vérifiez votre nom, promotion et niveau.",
        )

    university_name = None
    if student.university_id:
        uni = db.query(University).filter(University.id == student.university_id).first()
        if uni:
            university_name = uni.name

    return StudentOut(
        full_name=student.full_name,
        promotion=student.promotion,
        level=student.level,
        option=student.option,
        section=student.section,
        university=university_name,
        results=[
            ResultOut(
                course_name=r.course_name,
                semester=r.semester,
                score=r.score,
                grade=r.grade,
                credits=r.credits,
            )
            for r in student.results
        ],
    )


@router.get("/universities")
def list_universities(db: Session = Depends(get_db)):
    return [{"id": u.id, "name": u.name, "logo_url": u.logo_url} for u in db.query(University).all()]


@router.get("/promotions")
def list_promotions(db: Session = Depends(get_db)):
    rows = db.query(Student.promotion).distinct().all()
    db_vals = sorted([r[0] for r in rows if r[0]])
    defaults = ['2024-2025', '2023-2024', '2022-2023']
    return sorted(list(dict.fromkeys(defaults + db_vals)))


@router.get("/levels")
def list_levels(db: Session = Depends(get_db)):
    rows = db.query(Student.level).distinct().all()
    db_vals = sorted([r[0] for r in rows if r[0]])
    defaults = ['L1', 'L2', 'L3', 'M1', 'M2']
    return sorted(list(dict.fromkeys(defaults + db_vals)))


@router.get("/options")
def list_options(db: Session = Depends(get_db)):
    rows = db.query(Student.option).distinct().all()
    db_vals = sorted([r[0] for r in rows if r[0]])
    defaults = [
        'Français-langues africaines',
        'Anglais – cultures africaines',
        'Psycho pédagogie',
        'Histoire-Sciences sociales',
        'Géographie & Gestion Environnement',
        'Biologie & Technique appliquées',
        'Chimie Physique',
        'Chimie biologie',
        'Chimie alimentaire',
        'Chimie science de la terre',
        'Sciences de la Vie et de la terre',
        'Mathématiques',
        'Mathématiques – Physique',
        'Mathématiques – Informatique',
        'Informatique – Technologie',
        'Informatique – Mathématique',
        'Physique – Informatique',
        'Physique et Technologie',
        'Physique – Chimie',
        'Sciences commerciales & administratives',
        'Informatique de Gestion',
        'Gestion des entreprises',
        'Hôtellerie & restauration',
        'Accueil & tourisme',
        'Gestion Entreprises Touristiques & hôtelières',
    ]
    return sorted(list(dict.fromkeys(defaults + db_vals)))


@router.get("/sections")
def list_sections(db: Session = Depends(get_db)):
    rows = db.query(Student.section).distinct().all()
    db_vals = sorted([r[0] for r in rows if r[0]])
    defaults = [
        'Lettres & Sciences Humaines',
        'Sciences Exactes',
        'Sciences Commerciales & Informatique',
        'Sciences & Techniques d\'Accueil',
        'Section Soir',
    ]
    return sorted(list(dict.fromkeys(defaults + db_vals)))
