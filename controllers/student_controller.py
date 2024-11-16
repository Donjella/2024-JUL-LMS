from flask import Blueprint

from init import db
from models.student import Student, students_schema, student_schema

students_bp = Blueprint("students", __name__, url_prefix="/students")

# Read all - /students - GET
# Read one - /students/id - GET
# Create - /students - POST
# Update - /students/id - PUT, PATCH
# Delete - /students/id - DELETE


# Read all - /students - GET
@students_bp.route("/")
def get_students():
    stmt = db.select(Student)
    students_list = db.session.scalars(stmt)
    data = students_schema.dump(students_list)
    return data


# Read one - /students/id - GET
@students_bp.route("/<int:student_id>")
def get_student(student_id):
    stmt = db.select(Student).filter_by(id=student_id)
    student = db.session.scalar(stmt)
    if student:
        data = student_schema.dump(student)
        return data
    else:
        return {"message": f"Student with id {student_id} does not exist"}, 404