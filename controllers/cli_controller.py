from flask import Blueprint

from init import db
from models.student import Student
from models.teacher import Teacher

db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")


@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")


@db_commands.cli.command("seed")
def seed_tables():

    students = [
        Student(
            name="Student 1",
            email="student1@email.com",
            address="Sydney"
        ),
        Student(
            name="Student 2",
            email="student2@email.com",
            address="Melbourne"
        )
    ]

    db.session.add_all(students)

    teachers = [
        Teacher(
            name="Teacher 1",
            department="Engineering",
            address="Sydney"
        ),
        Teacher(
            name="Teacher 2",
            department="Management",
            address="Melbourne"
        )
    ]

    db.session.add_all(teachers)

    db.session.commit()

    print("Tables seeded")