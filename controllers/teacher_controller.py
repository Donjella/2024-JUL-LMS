from flask import Blueprint

from init import db
from models.teacher import Teacher, teachers_schema, teacher_schema

teachers_bp = Blueprint("teachers", __name__, url_prefix="/teachers")

# Create - /teachers - POST
# Read all - /teachers - GET
# Read one - /teachers/id - GET
# Update - /teachers/id - PUT, PATCH
# Delete - /teachers/id - DELETE


# Read all - /teachers - GET
@teachers_bp.route("/")
def get_teachers():
    stmt = db.select(Teacher)
    teachers_list = db.session.scalars(stmt)
    data = teachers_schema.dump(teachers_list) # handle a list of teachers, hence plural
    return data

# Read one - /teachers/id - GET
@teachers_bp.route("/<int:teacher_id>")
def get_teacher(teacher_id):
    stmt = db.select(Teacher).filter_by(id=teacher_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        return teacher_schema.dump(teacher)
    else:
        return{"message": f"Teacher with id {teacher_id} does not exist"}