from marshmallow import fields

from init import db, ma


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    department = db.Column(db.String, nullable=False)
    address = db.Column(db.String)

    # similarly, "Course" refers to the course model and we need to make sure that it needs the teacher field in Courseschema
    # "courses" needs to be included in CourseSchema's field
    courses = db.relationship("Course", back_populates="teacher")

    # id: 1,
# name: "Teacher 1",
# department: "Engineering",
# address: "Sydney",
# courses: [
#   {
#       id: 1,
#       name: "Course 1"
#   },
#   {
#       id: 2,
#       name: "Course 2"
#   }
# ]

class TeacherSchema(ma.Schema):
    courses = fields.List(fields.Nested("CourseSchema", exclude=["teacher"]))
    class Meta:
        fields = ("id", "name", "department", "address", "courses")

teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)