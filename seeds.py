from db import Teacher, Group, Student, Discipline, Grade
from datetime import date 
from faker import Faker
from sqlalchemy import select
from random import choice, randint

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:567432@localhost:5432/postgres")
Session = sessionmaker(bind=engine)
session = Session()


fake = Faker()


def fill_data():
    disciplines = [
        "Вища математика",
        "Хімія",
        "Економіка підприємства",
        "Обчислювальна математика",
        "Історія України",
        "Теоретична механіка",
        "Менеджмент організацій",
        "Системне програмування",
    ]

    groups = ["ВВ1", "ДД33", "АА5"]

    fake = Faker()
    number_of_teachers = 5
    number_of_students = 50

    def seed_teachers():
        for _ in range(number_of_teachers):
            teacher = Teacher(fullname=fake.name())
            session.add(teacher)
        session.commit()

    def seed_disciplines():
        teacher_ids = session.scalars(select(Teacher.id)).all()
        for discipline in disciplines:
            session.add(Discipline(name=discipline, teacher_id=choice(teacher_ids)))
        session.commit()

    def seed_groups():
        for group in groups:
            session.add(Group(name=group))
        session.commit()

    def seed_students():
        group_ids = session.scalars(select(Group.id)).all()
        for _ in range(number_of_students):
            student = Student(fullname=fake.name(), group_id=choice(group_ids))
            session.add(student)
        session.commit()

    def seed_grades():
        discipline_ids = session.scalars(select(Discipline.id)).all()
        student_ids = session.scalars(select(Student.id)).all()
        for _ in range(50):
            grade = Grade(
                grade=randint(1, 12),
                date_of=date.today(),
                student_id=choice(student_ids),
                discipline_id=choice(discipline_ids),
            )
            session.add(grade)
        session.commit()

    seed_teachers()
    seed_disciplines()
    seed_groups()
    seed_students()
    seed_grades()



if __name__ == "__main__":
    fill_data()