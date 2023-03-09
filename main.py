from sqlalchemy import func, desc, select, and_

from db import Student, Grade, Discipline, Group, Teacher
from seeds import session


def select_one():
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return result


def select_two(discipline_id: int):
    r = session.query(Discipline.name,
                      Student.fullname,
                      func.round(func.avg(Grade.grade), 2).label('avg_grade')
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Student.id, Discipline.name) \
        .order_by(desc('avg_grade')) \
        .limit(1).all()
    return r


def select_three(discipline_id: int):
    r = session.query(Discipline.name,
                      Group.name,
                      func.round(func.avg(Grade.grade), 2).label('avg_grade')
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Group.id, Discipline.name) \
        .order_by(desc('avg_grade')) \
        .all()
    return r

def select_four():
    r = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')).all()
    return r


def select_five():
    r = session.query(Discipline.name, Teacher.fullname) \
        .select_from(Discipline) \
        .join(Teacher) \
        .all()
    return r


def select_six():
    r = session.query(Student.fullname, Group.name) \
        .select_from(Student) \
        .join(Group) \
        .all()
    return r

def select_seven():
    r = session.query(Discipline.name,
                      Student.fullname,
                      Group.name,
                      Grade.date_of,
                      Grade.grade
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group) \
        .filter(and_(Discipline.name == "Вища математика", Group.name == "ВВ1")) \
        .all()
    return r

def select_eight():
    r = session.query(Teacher.fullname,
                      func.round(func.avg(Grade.grade), 2).label('avg_grade')
                      ) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Teacher) \
        .group_by(Teacher.id) \
        .all()
    return r

def select_nine():
    r = session.query(Student.fullname,
                      Discipline.name
                      ) \
        .select_from(Student) \
        .join(Grade) \
        .join(Discipline) \
        .filter(Student.fullname == "Іванов Іван Іванович") \
        .all()
    return r

def select_last(discipline_id, group_id):
    subquery = (select(Grade.date_of).join(Student).join(Group).where(
        and_(Grade.discipline_id == discipline_id, Group.id == group_id)
    ).order_by(desc(Grade.date_of)).limit(1).scalar_subquery())

    r = session.query(Discipline.name,
                      Student.fullname,
                      Group.name,
                      Grade.date_of,
                      Grade.grade
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group)\
        .filter(and_(Discipline.id == discipline_id, Group.id == group_id, Grade.date_of == subquery)) \
        .order_by(desc(Grade.date_of)) \
        .all()
    return r


if __name__ == '__main__':
    print(select_one())
    print(select_two(1))
    print(select_three(1))
    print(select_four())
    print(select_five())
    print(select_six())
    print(select_seven())
    print(select_eight())
    print(select_nine())
    print(select_last(1, 1))