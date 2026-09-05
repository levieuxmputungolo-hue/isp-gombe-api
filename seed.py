"""Seed sample data for testing."""
from app.db import SessionLocal, init_db
from app.models import University, Student, Result


def seed():
    init_db()
    db = SessionLocal()

    if db.query(Student).count() > 0:
        db.query(Result).delete()
        db.query(Student).delete()
        db.query(University).delete()
        db.commit()

    uni = University(name="Université de Kinshasa", logo_url="")
    db.add(uni)
    db.flush()

    students_data = [
        ("Mputu Ngolo Levieux", "2024-2025", "L1", "Gestion des Entreprise", "A", uni.id),
        ("Mukendi Jean-Paul", "2024-2025", "L1", "Informatique de Gestion", "A", uni.id),
        ("Kabongo Marie", "2024-2025", "L1", "Gestion des Entreprise", "B", uni.id),
        ("Ntumba Pierre", "2024-2025", "L2", "Informatique de Gestion", "A", uni.id),
        ("Mbala Alice", "2023-2024", "L2", "Gestion des Entreprise", "A", uni.id),
        ("Likulia David", "2023-2024", "L3", "Informatique de Gestion", "B", uni.id),
        ("Tshisekedi Grace", "2024-2025", "L3", "Gestion des Entreprise", "A", uni.id),
        ("Kabila Esther", "2024-2025", "L1", "Gestion des Entreprise", "A", uni.id),
        ("Ilunga Paulin", "2023-2024", "L2", "Informatique de Gestion", "B", uni.id),
    ]

    courses_by_level = {
        "L1": [
            ("Mathématiques Générales", 15.5, "B+", 6),
            ("Physique Fondamentale", 14.0, "B", 6),
            ("Informatique de Base", 16.0, "A-", 5),
            ("Anglais Scientifique", 12.5, "C+", 3),
            ("Introduction au Droit", 13.0, "B-", 4),
        ],
        "L2": [
            ("Analyse Numérique", 14.5, "B", 6),
            ("Mécanique Quantique", 13.0, "B-", 6),
            ("Base de Données", 17.0, "A", 5),
            ("Réseaux", 15.0, "B+", 5),
            ("Statistiques", 12.0, "C+", 4),
            ("Programmation Orientée Objet", 16.5, "A-", 5),
        ],
        "L3": [
            ("Intelligence Artificielle", 18.0, "A+", 6),
            ("Sécurité des Systèmes", 14.0, "B", 5),
            ("Génie Logiciel", 15.5, "B+", 5),
            ("Projet de Fin de Cycle", 16.0, "A-", 8),
            ("Stage Professionnel", 17.5, "A", 6),
            ("Droit des Affaires", 11.0, "C", 3),
        ],
    }

    for name, promotion, level, option, section, uid in students_data:
        student = Student(
            full_name=name,
            promotion=promotion,
            level=level,
            option=option,
            section=section,
            university_id=uid,
        )
        db.add(student)
        db.flush()

        courses = courses_by_level.get(level, [])
        for course_name, score, grade, credits in courses:
            result = Result(
                student_id=student.id,
                course_name=course_name,
                semester="S1",
                score=score,
                grade=grade,
                credits=credits,
            )
            db.add(result)

    db.commit()
    db.close()
    print("Seed completed successfully!")


if __name__ == "__main__":
    seed()
