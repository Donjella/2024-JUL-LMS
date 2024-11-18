from init import db, ma #db is an instance of SQLalchemy initialised in init.py

class Teacher(db.model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    department = db.Column(db.String, nullable=False)
    address = db.Column(db.String)

class TeacherSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "department", "address")

teacher_schema = TeacherSchema()
teacher_schema = TeacherSchema(many=True)