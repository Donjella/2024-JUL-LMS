from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

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
        return {"message": f"Teacher with id {teacher_id} does not exist"}, 404


# Create - /teachers - POST
@teachers_bp.route("/", methods=["POST"])
def create_teacher():
    try:
        body_data = request.get_json()
        new_teacher = Teacher(
            name=body_data.get("name"),
            department=body_data.get("department"),
            address=body_data.get("address"),
        )
        db.session.add(new_teacher)
        db.session.commit()

        return teacher_schema.dump(new_teacher), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The '{err.orig.diag.column_name}' is required"}, 409 # diagnostic diag.column_name to know it is due from column name see: https://www.psycopg.org/docs/extensions.html#psycopg2.extensions.Diagnostics