from app.db import SessionLocal
from app.models import Student, Result, University


def seed():
    db = SessionLocal()
    if db.query(Student).count() > 0:
        db.close()
        return

    uni = University(name="ISP-GOMBE", logo_url="/images/logo.png")
    db.add(uni)
    db.flush()

    students_data = [
        {
            "matricule": "222546",
            "full_name": "MPUTU NGOLA LE VIEUX",
            "promotion": "L1",
            "level": "L1",
            "option": "Informatique de Gestion",
            "section": "Sciences Commerciales & Informatique",
            "annee_academique": "2023-2024",
            "results": [
                {"code_ue": "MAT121", "intitule_ue": "MATHEMATIQUES APPLIQUEES", "bci": "Mathematiques Generales", "categorie": "A", "credits": 2, "note": 7, "session": "Normal"},
                {"code_ue": "MAT121", "intitule_ue": "MATHEMATIQUES APPLIQUEES", "bci": "Mathematiques Financieres", "categorie": "A", "credits": 1, "note": 5, "session": "Normal"},
                {"code_ue": "BUS111", "intitule_ue": "INTRODUCTION A LA GESTION", "bci": "Principes de Management", "categorie": "A", "credits": 2, "note": 8, "session": "Normal"},
                {"code_ue": "BUS111", "intitule_ue": "INTRODUCTION A LA GESTION", "bci": "Organisation des Entreprises", "categorie": "A", "credits": 1, "note": 6, "session": "Normal"},
                {"code_ue": "LAN121", "intitule_ue": "ANGLAIS APPLIQUE", "bci": "Anglais General", "categorie": "B", "credits": 2, "note": 6, "session": "Normal"},
                {"code_ue": "LAN121", "intitule_ue": "ANGLAIS APPLIQUE", "bci": "Anglais des Affaires", "categorie": "B", "credits": 1, "note": 4, "session": "Normal"},
                {"code_ue": "INF101", "intitule_ue": "INITIATION A L'INFORMATIQUE", "bci": "Systeme d'exploitation", "categorie": "A", "credits": 2, "note": 9, "session": "Normal"},
                {"code_ue": "INF101", "intitule_ue": "INITIATION A L'INFORMATIQUE", "bci": "Traitement de texte", "categorie": "B", "credits": 1, "note": 8, "session": "Normal"},
                {"code_ue": "ECO101", "intitule_ue": "ECONOMIE GENERALE", "bci": "Microeconomie", "categorie": "A", "credits": 2, "note": 5, "session": "Normal"},
                {"code_ue": "ECO101", "intitule_ue": "ECONOMIE GENERALE", "bci": "Macroéconomie", "categorie": "A", "credits": 1, "note": 4, "session": "Normal"},
                {"code_ue": "DRO101", "intitule_ue": "DROIT GENERAL", "bci": "Droit Civil", "categorie": "A", "credits": 2, "note": 6, "session": "Normal"},
                {"code_ue": "DRO101", "intitule_ue": "DROIT GENERAL", "bci": "Droit Constitutionnel", "categorie": "B", "credits": 1, "note": 5, "session": "Normal"},
                {"code_ue": "COM101", "intitule_ue": "COMPTABILITE GENERALE", "bci": "Comptabilite Base", "categorie": "A", "credits": 2, "note": 7, "session": "Normal"},
                {"code_ue": "COM101", "intitule_ue": "COMPTABILITE GENERALE", "bci": "Balance generale", "categorie": "A", "credits": 1, "note": 6, "session": "Normal"},
                {"code_ue": "MAT122", "intitule_ue": "MATHEMATIQUES FINANCIERES", "bci": "Interets simples", "categorie": "A", "credits": 2, "note": 5, "session": "Normal"},
                {"code_ue": "MAT122", "intitule_ue": "MATHEMATIQUES FINANCIERES", "bci": "Interets composes", "categorie": "A", "credits": 1, "note": 4, "session": "Normal"},
                {"code_ue": "STA101", "intitule_ue": "STATISTIQUES DESCRIPTIVES", "bci": "Statistiques univariees", "categorie": "A", "credits": 2, "note": 6, "session": "Normal"},
                {"code_ue": "STA101", "intitule_ue": "STATISTIQUES DESCRIPTIVES", "bci": "Diagrams et tableaux", "categorie": "B", "credits": 1, "note": 5, "session": "Normal"},
            ],
        },
        {
            "matricule": "223100",
            "full_name": "KALALA MBAYO JEAN",
            "promotion": "L1",
            "level": "L1",
            "option": "Informatique de Gestion",
            "section": "Sciences Commerciales & Informatique",
            "annee_academique": "2023-2024",
            "results": [
                {"code_ue": "MAT121", "intitule_ue": "MATHEMATIQUES APPLIQUEES", "bci": "Mathematiques Generales", "categorie": "A", "credits": 2, "note": 12, "session": "Normal"},
                {"code_ue": "MAT121", "intitule_ue": "MATHEMATIQUES APPLIQUEES", "bci": "Mathematiques Financieres", "categorie": "A", "credits": 1, "note": 10, "session": "Normal"},
                {"code_ue": "BUS111", "intitule_ue": "INTRODUCTION A LA GESTION", "bci": "Principes de Management", "categorie": "A", "credits": 2, "note": 14, "session": "Normal"},
                {"code_ue": "BUS111", "intitule_ue": "INTRODUCTION A LA GESTION", "bci": "Organisation des Entreprises", "categorie": "A", "credits": 1, "note": 13, "session": "Normal"},
                {"code_ue": "LAN121", "intitule_ue": "ANGLAIS APPLIQUE", "bci": "Anglais General", "categorie": "B", "credits": 2, "note": 11, "session": "Normal"},
                {"code_ue": "LAN121", "intitule_ue": "ANGLAIS APPLIQUE", "bci": "Anglais des Affaires", "categorie": "B", "credits": 1, "note": 10, "session": "Normal"},
                {"code_ue": "INF101", "intitule_ue": "INITIATION A L'INFORMATIQUE", "bci": "Systeme d'exploitation", "categorie": "A", "credits": 2, "note": 15, "session": "Normal"},
                {"code_ue": "INF101", "intitule_ue": "INITIATION A L'INFORMATIQUE", "bci": "Traitement de texte", "categorie": "B", "credits": 1, "note": 14, "session": "Normal"},
                {"code_ue": "ECO101", "intitule_ue": "ECONOMIE GENERALE", "bci": "Microeconomie", "categorie": "A", "credits": 2, "note": 11, "session": "Normal"},
                {"code_ue": "ECO101", "intitule_ue": "ECONOMIE GENERALE", "bci": "Macroéconomie", "categorie": "A", "credits": 1, "note": 9, "session": "Normal"},
                {"code_ue": "DRO101", "intitule_ue": "DROIT GENERAL", "bci": "Droit Civil", "categorie": "A", "credits": 2, "note": 13, "session": "Normal"},
                {"code_ue": "DRO101", "intitule_ue": "DROIT GENERAL", "bci": "Droit Constitutionnel", "categorie": "B", "credits": 1, "note": 12, "session": "Normal"},
                {"code_ue": "COM101", "intitule_ue": "COMPTABILITE GENERALE", "bci": "Comptabilite Base", "categorie": "A", "credits": 2, "note": 14, "session": "Normal"},
                {"code_ue": "COM101", "intitule_ue": "COMPTABILITE GENERALE", "bci": "Balance generale", "categorie": "A", "credits": 1, "note": 12, "session": "Normal"},
                {"code_ue": "MAT122", "intitule_ue": "MATHEMATIQUES FINANCIERES", "bci": "Interets simples", "categorie": "A", "credits": 2, "note": 11, "session": "Normal"},
                {"code_ue": "MAT122", "intitule_ue": "MATHEMATIQUES FINANCIERES", "bci": "Interets composes", "categorie": "A", "credits": 1, "note": 10, "session": "Normal"},
                {"code_ue": "STA101", "intitule_ue": "STATISTIQUES DESCRIPTIVES", "bci": "Statistiques univariees", "categorie": "A", "credits": 2, "note": 13, "session": "Normal"},
                {"code_ue": "STA101", "intitule_ue": "STATISTIQUES DESCRIPTIVES", "bci": "Diagrams et tableaux", "categorie": "B", "credits": 1, "note": 11, "session": "Normal"},
            ],
        },
        {
            "matricule": "224001",
            "full_name": "KABAMBA LUKUSA SARAH",
            "promotion": "L2",
            "level": "L2",
            "option": "Gestion des entreprises",
            "section": "Sciences Commerciales & Informatique",
            "annee_academique": "2023-2024",
            "results": [
                {"code_ue": "COM201", "intitule_ue": "COMPTABILITE ANALYTIQUE", "bci": "Analyse des charges", "categorie": "A", "credits": 2, "note": 15, "session": "Normal"},
                {"code_ue": "COM201", "intitule_ue": "COMPTABILITE ANALYTIQUE", "bci": "Calcul des couts", "categorie": "A", "credits": 1, "note": 14, "session": "Normal"},
                {"code_ue": "GES201", "intitule_ue": "GESTION DES RESSOURCES HUMAINES", "bci": "Recrutement", "categorie": "A", "credits": 2, "note": 16, "session": "Normal"},
                {"code_ue": "GES201", "intitule_ue": "GESTION DES RESSOURCES HUMAINES", "bci": "Administration du personnel", "categorie": "A", "credits": 1, "note": 15, "session": "Normal"},
                {"code_ue": "FIN201", "intitule_ue": "FINANCES Publiques", "bci": "Budget de l'Etat", "categorie": "B", "credits": 2, "note": 12, "session": "Normal"},
                {"code_ue": "FIN201", "intitule_ue": "FINANCES Publiques", "bci": "Fiscalite", "categorie": "B", "credits": 1, "note": 13, "session": "Normal"},
                {"code_ue": "DRO201", "intitule_ue": "DROIT DES AFFAIRES", "bci": "Droit commercial", "categorie": "A", "credits": 2, "note": 14, "session": "Normal"},
                {"code_ue": "DRO201", "intitule_ue": "DROIT DES AFFAIRES", "bci": "Droit du travail", "categorie": "A", "credits": 1, "note": 13, "session": "Normal"},
                {"code_ue": "ECO201", "intitule_ue": "ECONOMIE DES ENTREPRISES", "bci": "Strategie d'entreprise", "categorie": "A", "credits": 2, "note": 12, "session": "Normal"},
                {"code_ue": "ECO201", "intitule_ue": "ECONOMIE DES ENTREPRISES", "bci": "Marketing de base", "categorie": "B", "credits": 1, "note": 11, "session": "Normal"},
                {"code_ue": "MAT201", "intitule_ue": "MATHEMATIQUES APPLIQUEES II", "bci": "Algebre lineaire", "categorie": "A", "credits": 2, "note": 10, "session": "Normal"},
                {"code_ue": "MAT201", "intitule_ue": "MATHEMATIQUES APPLIQUEES II", "bci": "Analyse differentielle", "categorie": "A", "credits": 1, "note": 9, "session": "Normal"},
                {"code_ue": "INF201", "intitule_ue": "BASES DE DONNEES", "bci": "Modele relationnel", "categorie": "A", "credits": 2, "note": 17, "session": "Normal"},
                {"code_ue": "INF201", "intitule_ue": "BASES DE DONNEES", "bci": "SQL et administration", "categorie": "A", "credits": 1, "note": 16, "session": "Normal"},
                {"code_ue": "STA201", "intitule_ue": "PROBABILITES ET STATISTIQUES", "bci": "Lois de probabilite", "categorie": "B", "credits": 2, "note": 11, "session": "Normal"},
                {"code_ue": "STA201", "intitule_ue": "PROBABILITES ET STATISTIQUES", "bci": "Inference statistique", "categorie": "B", "credits": 1, "note": 10, "session": "Normal"},
                {"code_ue": "ANG201", "intitule_ue": "ANGLAIS DES AFFAIRES", "bci": "Correspondance commerciale", "categorie": "B", "credits": 2, "note": 14, "session": "Normal"},
                {"code_ue": "ANG201", "intitule_ue": "ANGLAIS DES AFFAIRES", "bci": "Communication orale", "categorie": "B", "credits": 1, "note": 13, "session": "Normal"},
            ],
        },
    ]

    for sdata in students_data:
        student = Student(
            matricule=sdata["matricule"],
            full_name=sdata["full_name"],
            promotion=sdata["promotion"],
            level=sdata["level"],
            option=sdata["option"],
            section=sdata["section"],
            annee_academique=sdata["annee_academique"],
            university_id=uni.id,
        )
        db.add(student)
        db.flush()
        for rdata in sdata["results"]:
            r = Result(
                student_id=student.id,
                code_ue=rdata["code_ue"],
                intitule_ue=rdata["intitule_ue"],
                bci=rdata["bci"],
                categorie=rdata["categorie"],
                credits=rdata["credits"],
                note=rdata["note"],
                session=rdata["session"],
                note_ponderee=rdata["note"] * rdata["credits"],
            )
            db.add(r)

    db.commit()
    db.close()
    print(f"[SEED] {len(students_data)} etudiants inseres avec succes.")
