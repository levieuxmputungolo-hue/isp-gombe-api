from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class University(Base):
    __tablename__ = "universities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    logo_url = Column(String, default="")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False, index=True)
    promotion = Column(String, nullable=False, index=True)
    level = Column(String, nullable=False, index=True)
    option = Column(String, nullable=False, default="")
    section = Column(String, nullable=False, default="")
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=True)
    results = relationship("Result", back_populates="student")


class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_name = Column(String, nullable=False)
    semester = Column(String, default="")
    score = Column(Float, nullable=False)
    grade = Column(String, default="")
    credits = Column(Integer, default=0)
    student = relationship("Student", back_populates="results")
