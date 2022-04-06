from flask import Flask, render_template, abort, request, redirect
from markupsafe import escape
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from os import getenv
from forms import csrf, LoginForm, CreateCourseForm

app = Flask(__name__)

db_url = getenv('DATABASE_URL', 'sqlite:///db.sqlite')
if db_url and db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SECRET_KEY'] = getenv('APP_SECRET_KEY')

db = SQLAlchemy(app)
login_manager = LoginManager(app)

csrf.init_app(app)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cover = db.Column(db.Text)
    is_new = db.Column(db.Boolean, default=False)
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lessons = db.relationship('Lesson', backref='course')


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    nickname = db.Column(db.String(32), unique=True)
    courses = db.relationship('Course', backref='owner')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


db.create_all()


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
