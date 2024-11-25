# Importing built-in modules (no installation needed)
import os 

# Importing third-party libraries (require installation via pip)
from flask import Flask

# Importing internal modules/files (created within the project)
from init import db, ma
from controllers.cli_controller import db_commands
from controllers.student_controller import students_bp
from controllers.teacher_controller import teachers_bp
from controllers.course_controller import courses_bp
from controllers.enrolment_controller import enrolment_bp


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(students_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(enrolment_bp)


    return app