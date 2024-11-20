from flask import Blueprint

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