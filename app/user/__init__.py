from flask import Blueprint

user_bp = Blueprint('user',__name__)
course_bp = Blueprint('course_bp',__name__)
student_bp = Blueprint('student',__name__)

from . import controller
