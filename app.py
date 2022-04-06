from flask import Flask, render_template, abort, request, redirect
from markupsafe import escape
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from os import getenv
from models import db, User, Lesson, Course
from forms import csrf, LoginForm, CreateCourseForm

app = Flask(__name__)

db_url = getenv('DATABASE_URL', 'sqlite:///db.sqlite')
if db_url and db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SECRET_KEY'] = getenv('APP_SECRET_KEY')

login_manager = LoginManager(app)

db.app = app
db.init_app(app)
db.create_all()
csrf.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def homepage():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me') is not None
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember_me)
            return redirect('/')
    return render_template('login.html', form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/search')
def search():
    text = escape(request.args['text'])
    courses = Course.query.all()
    selected_courses = [course for course in courses if text in course['name'] or text in course['desc']]
    return render_template('search.html', text=text, courses=selected_courses)


@app.route('/courses')
def get_courses():
    return 'All my courses'


@app.route('/courses/create', methods=['GET', 'POST'])
@login_required
def create_course():
    create_course_form = CreateCourseForm()
    if create_course_form.validate_on_submit():
        new_course = Course()
        new_course.name = request.form.get('name')
        new_course.description = request.form.get('description')
        new_course.cover = request.form.get('cover')
        new_course.is_new = request.form.get('is_new') is not None
        new_course.date_start = datetime.fromisoformat(request.form.get('date_start'))
        new_course.date_end = datetime.fromisoformat(request.form.get('date_end'))
        new_course.owner_id = current_user.id
        db.session.add(new_course)
        db.session.commit()
        return redirect('/')
    return render_template('create_course.html', form=create_course_form)


@app.route('/courses/<int:course_id>')
def get_course(course_id):
    course = Course.query.get(course_id)
    return render_template('course.html', course=course)


@app.errorhandler(404)
def handle_404(error):
    return render_template('404.html'), 404


@app.template_filter('datetime')
def datetime_format(value, format="%c"):
    return value.strftime(format)


if __name__ == '__main__':
    app.run()
