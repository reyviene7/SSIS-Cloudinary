from flask import render_template, redirect, request, jsonify, url_for, flash, session
from . import user_bp
import app.models as models
from app.models import m_college, m_course, m_student, Users
from app.user.forms import UserForm
import bcrypt
from app import login_manager
from app import mysql
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
import re

@user_bp.route('/')
def index():
    return render_template('index.html', title='Home')

@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id)

@user_bp.route('/login_page', methods=['GET', 'POST'])
def login_page():
    msg=''
    cursor = mysql.connection.cursor()
    if current_user.is_authenticated:
        return redirect(url_for('user.college_db'))

    form = UserForm(request.form)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s',(username,password))
        record = cursor.fetchone()
        if record:
            session['loggedin']= True
            session['username']= record[1]
            return redirect(url_for('user.college_db'))
        else:
            flash('Incorrect username or password. Try it again!', 'error')

    return render_template('login_page.html', title='Login', form=form, msg=msg)

@user_bp.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('user.index'))

@user_bp.route('/signup', methods=['GET','POST'])
def signup():
    msg=''
    cursor = mysql.connection.cursor()
    form = UserForm(request.form)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        cursor.execute('SELECT * FROM users WHERE email=%s',(email,))
        record = cursor.fetchone()
        
        if record:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return redirect(url_for('user.login_page'))

    elif request.method == 'POST':
        msg = 'Please fill out the form !'

    account = Users.get_users()
    
    return render_template('login_page.html', title='Sign Up', form=form, account=account, msg=msg)

@user_bp.route('/college', methods=['GET', 'POST'])
def college_db():
    try:
        username = session['username']
    except KeyError:
        return redirect(url_for('user.login_page'))
    if request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        
        if not code or not name:
            flash('Please fill in all fields.')
            return redirect(url_for('user.college_db'))
        
        m_college.create(code, name)
        flash('College created Successfully!')
        return redirect(url_for('user.college_db'))

    colleges = m_college.get_colleges()     
    print(colleges)
    return render_template('college.html', username=username, colleges=colleges, title='College',something='something')

@user_bp.route('/college/delete_college/<string:college_code>', methods=['DELETE'])
def delete_college(college_code):
    if request.method == 'DELETE':
        flash('College has been deleted Successfully!')
        result = m_college.delete_college(college_code)
        response = jsonify(result)
        return response
    
@user_bp.route('/college/<string:college_code>', methods=['GET', 'POST'])
def update_college(college_code):
    if request.method == 'POST':
        new_code = request.form.get('code')
        new_name = request.form.get('name')
        m_college.update_college(college_code, new_code, new_name)
        return redirect(url_for('user.college_db'))
    college = m_college.get_college_by_code(college_code)
    return render_template('college.html', college=college)

@user_bp.route('/search_college', methods=['GET'])
def search_college():
    search_query = request.args.get('search')
    filter_by = request.args.get('filter_by')
    
    if filter_by == 'code':
        colleges = m_college.search_colleges_by_code(search_query)
    else:
        colleges = m_college.search_colleges_by_name(search_query)
    
    return render_template('college.html', colleges=colleges, title="College", selected_filter=filter_by)

@user_bp.route('/course', methods=['GET' , 'POST'])
def course():
    colleges = m_college.get_colleges()
    try:
        username = session['username']
    except KeyError:
        return redirect(url_for('user.login_page'))
    if request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        college = request.form.get('college')
        
        if not code or not name or not college:
            flash('Please fill in all fields.')
            return redirect(url_for('user.course'))
        
        m_course.create_course(code, name, college)
        flash('Course created Successfully!')
        return redirect(url_for('user.course'))

    courses = m_course.get_courses()
    print(courses)
    return render_template('course.html', courses=courses , username=username, title="Course", colleges=colleges)

@user_bp.route('/delete_course/<string:course_code>', methods=['DELETE'])
def delete_course(course_code):
    if request.method == 'DELETE':
        flash('College has been deleted Successfully!')
        result = m_course.delete_course(course_code)
        response = jsonify(result)
        return response
    
@user_bp.route('/update_course/<string:course_code>', methods=['POST'])
def update_course(course_code):
    new_code = request.form.get('code')
    new_name = request.form.get('name')
    new_college = request.form.get('college')
    m_course.update_course(course_code, new_code, new_name, new_college)
    courses = m_course.get_courses()
    colleges = m_college.get_colleges()
    return render_template('course.html', courses=courses, colleges=colleges)

@user_bp.route('/search_course', methods=['GET'])
def search_course():
    search_query = request.args.get('search')
    filter_by = request.args.get('filter_by')
    
    colleges = m_college.get_colleges()

    if filter_by == 'code':
        courses = m_course.search_courses_by_code(search_query)
    elif filter_by == 'name':
        courses = m_course.search_courses_by_name(search_query)
    elif filter_by == 'college':
        courses = m_course.search_courses_by_college(search_query)
    else:
        courses = m_course.get_courses()
    
    return render_template('course.html', courses=courses, colleges=colleges, title="Course",  selected_filter=filter_by)


@user_bp.route('/student', methods=['GET', 'POST'])
def student():
    courses = m_course.get_courses()
    
    try:
        username = session['username']
    except KeyError:
        return redirect(url_for('user.login_page'))

    if request.method == 'POST':
        id = request.form.get('id')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        course = request.form.get('course')
        year = request.form.get('year')
        gender = request.form.get('gender')
        
        if not id or not firstname or not lastname or not course or not year or not gender:
            flash('Please fill in all fields.')
            return redirect(url_for('user.student'))
        
        image_url = None
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                # Attempt to upload the image
                image_url = m_student.upload_image(image)

                # If the image upload fails (returns None), flash an error and do not create the student
                if image_url is None:
                    return redirect(request.url)

        # Set the default image URL
        default_image_url = "https://res.cloudinary.com/dzwjjpvdb/image/upload/v1702977617/SSIS_CLOUDINARY/user_profile_fcfymn.jpg"
        if image_url is None:
            image_url = default_image_url
            
        m_student.add_student(id, firstname, lastname, course, year, gender, image_url)

    students = m_student.get_students()
    print(students)
    return render_template('student.html', students=students, username=username, title="Student", courses=courses)

@user_bp.route('/delete_student/<string:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        result = m_student.delete_student(student_id)
        flash("Student is deleted")
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    
@user_bp.route('/update_student/<string:student_id>', methods=['POST'])
def update_student(student_id):
    new_id = request.form['id']
    new_firstname = request.form['firstname']
    new_lastname = request.form['lastname']
    new_course = request.form['course']
    new_year = request.form['year']
    new_gender = request.form['gender']
    
    # Get the existing student data
    existing_student = m_student.get_student_by_id(student_id)

    if 'image' in request.files:
        new_image = request.files['image']
        if new_image.filename != '':
            new_image_url = m_student.upload_image(new_image)
        else:
            new_image_url = existing_student.get('image_url')
    else:
        new_image_url = existing_student.get('image_url')
    
    m_student.update_student(student_id, new_id, new_firstname, new_lastname, new_course, new_year, new_gender, new_image_url)
    
    return redirect(url_for('user.student', student_id=student_id))

@user_bp.route('/search_student', methods=['GET'])
def search_student():
    courses = m_course.get_courses()

    if request.method == 'POST':
        search_query = request.form.get('search')
        filter_by = request.form.get('filter_by')
    else:
        search_query = request.args.get('search')
        filter_by = request.args.get('filter_by')    
    
    if filter_by == 'id':
        students = m_student.search_students_by_id(search_query)
    elif filter_by == 'firstname':
        students = m_student.search_students_by_firstname(search_query)
    elif filter_by == 'lastname':
        students = m_student.search_students_by_lastname(search_query)
    elif filter_by == 'course':
        students = m_student.search_students_by_course(search_query)
    elif filter_by == 'year':
        students = m_student.search_students_by_year(search_query)
    elif filter_by == 'gender':
        students = m_student.search_students_by_gender(search_query)
    else:
        students = m_student.get_students()
    
    return render_template('student.html', students=students, courses=courses, title="Student",  selected_filter=filter_by)
