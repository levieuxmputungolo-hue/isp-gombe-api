from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    matricule = Column(String, nullable=False, index=True)
    full_name = Column(String, nullable=False, index=True)
    promotion = Column(String, nullable=False, index=True)
    level = Column(String, nullable=False, index=True)
    option = Column(String, nullable=False, default="")
    section = Column(String, nullable=False, default="")
    annee_academique = Column(String, nullable=False, default="2024-2025")
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=True)
    results = relationship("Result", back_populates="student", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("matricule", "promotion", "annee_academique", name="uq_student_promo_annee"),
    )


class University(Base):
    __tablename__ = "universities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    logo_url = Column(String, default="")


class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    code_ue = Column(String, nullable=False)
    intitule_ue = Column(String, nullable=False)
    bci = Column(String, nullable=False)
    categorie = Column(String, nullable=False, default="A")
    credits = Column(Integer, nullable=False, default=0)
    note = Column(Float, nullable=False)
    session = Column(String, default="Normal")
    note_ponderee = Column(Float, default=0.0)
    student = relationship("Student", back_populates="results")


class SemesterReport(Base):
    __tablename__ = "semester_reports"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    semester = Column(String, nullable=False)
    annee_academique = Column(String, nullable=False)
    total_credits = Column(Integer, default=0)
    total_pondere = Column(Float, default=0.0)
    moyenne = Column(Float, default=0.0)
    moyenne_a = Column(Float, default=0.0)
    moyenne_b = Column(Float, default=0.0)
    decision = Column(String, default="")
    mention = Column(String, default="")
    credits_capitalises = Column(Integer, default=0)
    student = relationship("Student")
