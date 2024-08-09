from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from app import mysql
from flask import flash
from cloudinary import uploader
from config import CLOUDINARY_FOLDER
from werkzeug.utils import secure_filename
import bcrypt
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user

class Users(UserMixin):

    def __init__(self, id, username=None, password=None, email=None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    def add(cls, username, password, email):
        try: 
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("INSERT INTO users (username, password, email) VALUES (%s,%s,%s)", (username, password, email))
            mysql.connection.commit()
            cur.close()
            return "Account created successfully"
        except Exception as e:
            return f"Failed to create Account: {str(e)}"
    
    @classmethod
    def get_users(cls):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        return users
    
class m_college(object):
    @classmethod
    def create(cls, code, name):
        try: 
            cur =mysql.new_cursor(dictionary=True)
            cur.execute("INSERT INTO College (code, name) VALUES (%s,%s)", (code, name))
            mysql.connection.commit()
            cur.close()
            return "College created successfully"
        except Exception as e:
            return f"Failed to create College: {str(e)}"
    
    @classmethod
    def get_colleges(cls):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM college")
        colleges = cur.fetchall()
        cur.close()
        return colleges 
    
    @classmethod
    def delete_college(cls, college_code):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("DELETE FROM college WHERE code = %s", (college_code,))
            mysql.connection.commit()
            cur.close()
            return "College deleted successfully"
        except Exception as e:
            return f"Failed to delete College: {str(e)}"

    @classmethod
    def update_college(cls, college_code, new_code, new_name):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("UPDATE College SET code = %s, name = %s WHERE code = %s", (new_code, new_name, college_code))
            mysql.connection.commit()
            cur.close()
            return "College updated successfully"
        except Exception as e:
            return f"Failed to update College: {str(e)}"

    @classmethod
    def get_college_by_code(cls, code):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM college WHERE code = %s", (code,))
        college = cur.fetchone()
        cur.close()
        return college
    
    @classmethod
    def search_colleges_by_code(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM college WHERE code LIKE %s", (f"%{search_query}%",))
        colleges = cur.fetchall()
        cur.close()
        return colleges

    @classmethod
    def search_colleges_by_name(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM college WHERE name LIKE %s", (f"%{search_query}%",))
        colleges = cur.fetchall()
        cur.close()
        return colleges


class m_course:
    @classmethod
    def create_course(cls, code, name, college):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("INSERT INTO course (code, name, college) VALUES (%s, %s, %s)", (code, name, college))
            mysql.connection.commit()            
            return "Course created successfully"
        except Exception as e:
            return f"Failed to create course: {str(e)}"

    @classmethod
    def get_courses(cls):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM course")
        courses = cur.fetchall()
        return courses

    @classmethod
    def delete_course(cls, code):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("DELETE FROM course WHERE code = %s", (code,))
            mysql.connection.commit()
            cur.close()
            return {"success": True, "message": "Course deleted successfully"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    @classmethod
    def update_course(cls, course_code, new_code, new_name, new_college):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("UPDATE course SET code = %s, name = %s, college = %s WHERE code = %s", (new_code, new_name, new_college, course_code))
            mysql.connection.commit()
            cur.close()
            return "Course updated successfully"
        except Exception as e:
            return f"Failed to update course: {str(e)}"
    
    @classmethod
    def search_courses_by_code(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM course WHERE code LIKE %s", (f"%{search_query}%",))
        courses = cur.fetchall()
        cur.close()
        return courses

    @classmethod
    def search_courses_by_name(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM course WHERE name LIKE %s", (f"%{search_query}%",))
        courses = cur.fetchall()
        cur.close()
        return courses

    @classmethod
    def search_courses_by_college(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM course WHERE college LIKE %s", (f"%{search_query}%",))
        courses = cur.fetchall()
        cur.close()
        return courses

class m_student:
    @classmethod
    def add_student(cls, id, firstname, lastname, course_code, year, gender, image_url):
        try:
            cur = mysql.new_cursor(dictionary=True)

            # Check if the ID is already taken
            cur.execute("SELECT id FROM student WHERE id = %s", (id,))
            existing_id = cur.fetchone()
            if existing_id:
                flash("ID is already taken.", "error")
                return "Failed to create student"

            # Insert the new student record
            cur.execute("INSERT INTO student (id, firstname, lastname, course, year, gender, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (id, firstname, lastname, course_code, year, gender, image_url))
            mysql.connection.commit()
            
            return "Student created successfully"
        
        except Exception as e:
            flash("Failed to create student(models 1).", "error")
            return "Failed to create student"
    
    @classmethod
    def get_students(cls):
        cur = mysql.new_cursor(dictionary=True)
        query = """
        SELECT 
        student.id,
        student.firstname,
        student.lastname,
        student.year,
        student.gender,
        student.image_url,
            CONCAT(course_view.course_name, ' - ', course_view.college_code) AS course_and_college
        FROM 
                student
        LEFT JOIN 
                course_view ON student.course = course_view.course_code
        """
        cur.execute(query)
        students = cur.fetchall()
        return students
    
    @classmethod
    def get_collegelist(cls):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT college_code FROM course_view")
        students = cur.fetchall()
        return students
    
    @classmethod
    def search_students_by_id(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM student WHERE id LIKE %s", (f"%{search_query}%",))
        students = cur.fetchall()
        cur.close()
        return students

    @classmethod
    def search_students_by_firstname(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        query = """
        SELECT 
            student.*,
            CONCAT(course_view.course_name, ' - ', course_view.college_code) AS course_and_college
        FROM student
        LEFT JOIN course_view ON student.course = course_view.course_code
        WHERE student.firstname LIKE %s
        """
        cur.execute(query, (f"%{search_query}%",))
        students = cur.fetchall()
        cur.close()
        return students

    @classmethod
    def search_students_by_lastname(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        query = """
        SELECT 
            student.*,
            CONCAT(course_view.course_name, ' - ', course_view.college_code) AS course_and_college
        FROM student
        LEFT JOIN course_view ON student.course = course_view.course_code
        WHERE student.lastname LIKE %s
        """
        cur.execute(query, (f"%{search_query}%",))
        students = cur.fetchall()
        cur.close()
        return students

    @classmethod
    def search_students_by_course(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        query = """
        SELECT 
            student.*,
            CONCAT(course_view.course_name, ' - ', course_view.college_code) AS course_and_college
        FROM student
        LEFT JOIN course_view ON student.course = course_view.course_code
        WHERE course_view.course_name LIKE %s
        """
        cur.execute(query, (f"%{search_query}%",))
        students = cur.fetchall()
        cur.close()
        return students

    @classmethod
    def search_students_by_college(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        query = """
        SELECT student.*,
            CONCAT(course_view.course_name, ' - ', course_view.college_code) AS course_and_college
        FROM student
        LEFT JOIN course_view ON student.course = course_view.course_code
        WHERE course_view.college_code LIKE %s
        """
        cur.execute(query, (f"%{search_query}%",))
        students = cur.fetchall()
        cur.close()
        return students

    @classmethod
    def search_students_by_year(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM student WHERE year LIKE %s", (f"%{search_query}%",))
        students = cur.fetchall()
        cur.close()
        return students

    @classmethod
    def search_students_by_gender(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM student WHERE gender = %s", (search_query,))
        students = cur.fetchall()
        cur.close()
        return students
    
    @classmethod
    def update_student(cls, student_id, new_id, new_firstname, new_lastname, new_course, new_year, new_gender, new_image_url):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("SELECT id FROM student WHERE id = %s AND id != %s", (new_id, student_id))
            existing_id = cur.fetchone()
            if existing_id:
                flash("ID is already taken.", "error")
                return "Failed to update student"
            cur.execute("UPDATE student SET id=%s, firstname=%s, lastname=%s, course=%s, year=%s, gender=%s, image_url=%s WHERE id=%s",
                        (new_id, new_firstname, new_lastname, new_course, new_year, new_gender, new_image_url, student_id))

            mysql.connection.commit()
            cur.close()
            return "Student updated successfully"
        except Exception as e:
            return "Failed to update student"

    @classmethod
    def get_student_by_id(cls, student_id):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("SELECT * FROM student WHERE id = %s", (student_id,))
            student = cur.fetchone()
            cur.close()
            return student
        except Exception as e:
            flash("Failed to get student by ID.", "error")
            return None
        
    @classmethod
    def delete_student(cls, student_id):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("DELETE FROM student WHERE id = %s", (student_id,))
            mysql.connection.commit()
            cur.close()
            return {"success": True, "message": "Course deleted successfully"}
        except Exception as e:
            return {"success": False, "message": str(e)}
        
        
    @classmethod
    def upload_image(cls,image):
        try:
            allowed_extensions = {'png', 'jpg', 'jpeg'}
            if '.' in image.filename and image.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                max_file_size_mb = 1.0
                max_file_size_bytes = max_file_size_mb * 1024 * 1024  

                if len(image.read()) <= max_file_size_bytes:
                    image.seek(0)
                    filename = secure_filename(image.filename)
                    response = uploader.upload(image, folder=CLOUDINARY_FOLDER)  
                    return response['secure_url']
                else:
                    flash("File size exceeds the maximum allowed limit (1MB).", "error")
                    return None
            else:
                flash("Invalid file type. Please upload a valid image file (allowed types: png, jpg, jpeg).", "error")
                return None
        except Exception as e:
            flash("Failed to upload image. Please try again.", "error")
            return None