from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

# Подключение к SQLite
engine = create_engine("sqlite:///students.db")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# ------------------ Модель данных ------------------
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)
    faculty = Column(String)
    course = Column(String)
    grade = Column(Integer)

# Создание таблицы
Base.metadata.create_all(engine)

# ------------------ Импорт из CSV ------------------
def load_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        student = Student(
            last_name=row['Фамилия'],
            first_name=row['Имя'],
            faculty=row['Факультет'],
            course=row['Курс'],
            grade=int(row['Оценка'])
        )
        session.add(student)
    session.commit()

# ------------------ Запросы ------------------
def get_students_by_faculty(faculty_name):
    return session.query(Student).filter(Student.faculty == faculty_name).all()

def get_unique_courses():
    return session.query(Student.course).distinct().all()

def get_average_grade_by_faculty(faculty_name):
    records = session.query(Student.grade).filter(Student.faculty == faculty_name).all()
    grades = [r[0] for r in records]
    return sum(grades) / len(grades) if grades else 0

def get_students_with_low_grade(course_name):
    return session.query(Student).filter(Student.course == course_name, Student.grade < 30).all()

# ------------------ Пример использования ------------------
if __name__ == "__main__":
    load_from_csv("students.csv")

    print("Студенты АВТФ:")
    for s in get_students_by_faculty("АВТФ"):
        print(s.first_name, s.last_name)

    print("\nУникальные курсы:", get_unique_courses())
    print("\nСредний балл по ФПМИ:", get_average_grade_by_faculty("ФПМИ"))

    print("\nСтуденты с оценкой ниже 30 по Мат. Анализ:")
    for s in get_students_with_low_grade("Мат. Анализ"):
        print(s.first_name, s.last_name, s.grade)
