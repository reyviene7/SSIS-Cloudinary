from flask import Flask
from flask_mysql_connector import MySQL
from flask_bootstrap import Bootstrap
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY
from flask_wtf.csrf import CSRFProtect
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user

mysql = MySQL()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'user.login_page'

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['MYSQL_HOST'] = DB_HOST
    app.config['MYSQL_USER'] = DB_USERNAME
    app.config['MYSQL_PASSWORD'] = DB_PASSWORD
    app.config['MYSQL_DATABASE'] = DB_NAME
    
    bootstrap.init_app(app)
    mysql.init_app(app)
    CSRFProtect(app)
    login_manager.init_app(app)

    from .user import user_bp as user_blueprint
    from .user import course_bp as course_blueprint
    from .user import student_bp as student_blueprint
    app.register_blueprint(user_blueprint)
    app.register_blueprint(course_blueprint)
    app.register_blueprint(student_blueprint)
    

    return app
