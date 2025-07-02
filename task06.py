from fastapi import FastAPI, BackgroundTasks, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd
import redis
import json
from typing import List
import os

app = FastAPI()

# ------------------ Настройки БД ------------------
DATABASE_URL = "sqlite:///./students.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ------------------ Redis ------------------
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# ------------------ Модель ------------------
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    faculty = Column(String)
    course = Column(String)
    grade = Column(Integer)

Base.metadata.create_all(bind=engine)

# ------------------ Зависимость ------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ Фоновая задача: Загрузка из CSV ------------------
def load_students_background(csv_path: str):
    if not os.path.exists(csv_path):
        return
    df = pd.read_csv(csv_path)
    db = SessionLocal()
    for _, row in df.iterrows():
        student = Student(
            first_name=row['Имя'],
            last_name=row['Фамилия'],
            faculty=row['Факультет'],
            course=row['Курс'],
            grade=int(row['Оценка'])
        )
        db.add(student)
    db.commit()
    db.close()
    redis_client.delete("all_students")  # сброс кеша

@app.post("/load-csv")
def load_csv(csv_path: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(load_students_background, csv_path)
    return {"message": "Загрузка запущена"}

# ------------------ Фоновая задача: Удаление ------------------
def delete_students_background(ids: List[int]):
    db = SessionLocal()
    for student_id in ids:
        student = db.query(Student).filter(Student.id == student_id).first()
        if student:
            db.delete(student)
    db.commit()
    db.close()
    redis_client.delete("all_students")  # сброс кеша

@app.post("/delete-students")
def delete_students(ids: List[int], background_tasks: BackgroundTasks):
    background_tasks.add_task(delete_students_background, ids)
    return {"message": "Удаление запущено"}

# ------------------ Кешируемый эндпойнт ------------------
@app.get("/students")
def get_all_students():
    cached = redis_client.get("all_students")
    if cached:
        return json.loads(cached)

    db = SessionLocal()
    students = db.query(Student).all()
    result = [
        {
            "id": s.id,
            "first_name": s.first_name,
            "last_name": s.last_name,
            "faculty": s.faculty,
            "course": s.course,
            "grade": s.grade,
        } for s in students
    ]
    db.close()
    redis_client.set("all_students", json.dumps(result), ex=300)  # кеш на 5 минут
    return result
