from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./students.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI()

# ------------------ Модель SQLAlchemy ------------------
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    faculty = Column(String)
    course = Column(String)
    grade = Column(Integer)

Base.metadata.create_all(bind=engine)

# ------------------ Pydantic-схемы ------------------
class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    faculty: str
    course: str
    grade: int

class StudentUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    faculty: str = None
    course: str = None
    grade: int = None

# ------------------ Зависимость ------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ CRUD Эндпойнты ------------------
@app.post("/students/", response_model=dict)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return {"id": db_student.id, "message": "Student created"}

@app.get("/students/", response_model=list)
def read_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return [s.__dict__ for s in students]

@app.put("/students/{student_id}", response_model=dict)
def update_student(student_id: int, updates: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    for field, value in updates.dict(exclude_unset=True).items():
        setattr(student, field, value)

    db.commit()
    return {"message": "Student updated"}

@app.delete("/students/{student_id}", response_model=dict)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return {"message": "Student deleted"}
