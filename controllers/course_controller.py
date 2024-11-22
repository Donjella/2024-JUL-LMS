from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.course import Course, courses_schema, course_schema

# Create a Blueprint for course-related routes, with the "/courses" URL prefix
courses_bp = Blueprint("courses", __name__, url_prefix="/courses")

# Read all courses
# The route is "/" because the "/courses" prefix is already defined in the Blueprint
@courses_bp.route("/")
def get_courses():
    stmt = db.select(Course)
    courses_list = db.session.scalars(stmt)
    return courses_schema.dump(courses_list)


# Read one course
@courses_bp.route("/<int:course_id>")
def get_course(course_id):
    stmt = db.select(Course).filter_by(id=course_id)
    course = db.session.scalar(stmt)
    if course:
        return course_schema.dump(course)
    else:
        return {"message": f"Course with id {course_id} does not exist"}, 404
    
# Create
@courses_bp.route("/", methods=["POST"])
def create_course():
    try:
        # get the data from the request body
        body_data = request.get_json()
        # create a course instance, it must match values with body (JSON) in Inmsonia create post method for create course
        course = Course (
            name=body_data.get("name"),
            duration=body_data.get("duration"),
            teacher_id=body_data.get("teacher_id")
        )
        # add to session and commit
        db.session.add(course)
        db.session.commit()
        return course_schema.dump(course), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": "The name cannot be null"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Duplicate name"}, 409

# Delete
@courses_bp.route("/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    # find the course to delete
    stmt = db.select(Course).filter_by(id=course_id)
    course = db.session.scalar(stmt)
    # if the course exists
    if course:
        # delete
        db.session.delete(course)
        # commit
        db.session.commit()
        # return
        return {"message": f"Course '{course.name}' deleted successfully"}
    # else
    else:
        # return error response
        return {"message": f"Course with id {course_id} doesn't exist"}, 404