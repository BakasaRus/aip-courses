from flask import Flask, render_template, abort, request, redirect
from markupsafe import escape
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, TextAreaField, URLField, BooleanField, DateTimeLocalField, EmailField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_login import LoginManager, UserMixin, login_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'ghsgh srth rt drtyu dtrfy ue608d r6th 36dr06dr48t 58'
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)


courses = [
    {
        'id': 1,
        'name': 'Основы программирования на языке Kotlin',
        'desc': 'Курс посвящен изучению языка программирования Kotlin, передовому языку для проектирования различного рода приложений.',
        'img': 'https://cdn.openedu.ru/f1367c/CACHE/images/cover/c820f30eb3223c5142d5fc30c4c1a4383645c49c/f889db722db8aa0a207011ff80bf95f1.png',
        'is_new': False,
        'start': datetime.fromisoformat('2022-09-23T12:00:00'),
        'end': datetime.fromisoformat('2022-12-23T12:00:00'),
    },
    {
        'id': 2,
        'name': 'Разработка современных мобильных приложений на языке Kotlin',
        'desc': 'Курс посвящен изучению современных способов разработки мобильных приложений на языке Kotlin под ОС Android.',
        'img': 'https://cdn.openedu.ru/f1367c/CACHE/images/cover/318bd6f2d0bbe5b028a4c0d8688ed714684f4cb1/c12c48c9feac6b332fc1c8713ba8922b.png',
        'is_new': True,
        'start': datetime.now(),
        'end': datetime.now(),
    },
    {
        'id': 4,
        'name': 'Модели и методы аналитической механики',
        'desc': 'В курсе рассматриваются подходы к составлению математических моделей динамических систем и методы их математической обработки.',
        'img': 'https://cdn.openedu.ru/f1367c/CACHE/images/cover/badge_J6JVOr2/ce39a073a96624c22ce5203d473a2969.png',
        'is_new': True,
        'start': datetime.now(),
        'end': datetime.now(),
    },
    {
        'id': 5,
        'name': 'Введение в машинное обучение',
        'desc': 'Машинное обучение, его применение и совершенствование — это то, над чем трудятся многие лучшие умы современности.',
        'img': 'https://cdn.openedu.ru/f1367c/CACHE/images/cover/54eda2d1971ba38fd42e9c7afddf54e27f0b34fd/af28f10bf4a4454bfde701ae596c7f3d.png',
        'start': datetime.now(),
        'end': datetime.now(),
    }
]


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cover = db.Column(db.Text)
    is_new = db.Column(db.Boolean, default=False)
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
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


class CreateCourseForm(FlaskForm):
    name = StringField(label='Название курса', validators=[DataRequired()])
    description = TextAreaField(label='Описание', validators=[DataRequired()])
    cover = URLField(label='Ссылка на обложку', validators=[DataRequired(), URL()])
    is_new = BooleanField(label='Новый курс')
    date_start = DateTimeLocalField(label='Дата начала')
    date_end = DateTimeLocalField(label='Дата окончания')


class LoginForm(FlaskForm):
    email = EmailField(label='Электронная почта', validators=[DataRequired()])
    password = PasswordField(label='Пароль', validators=[DataRequired()])


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def homepage():  # put application's code here
    return render_template('index.html', courses=courses)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return redirect('/')
    return render_template('login.html', form=login_form)


@app.route('/search')
def search():
    text = escape(request.args['text'])
    selected_courses = [course for course in courses if text in course['name'] or text in course['desc']]
    return render_template('search.html', text=text, courses=selected_courses)


@app.route('/about')
def about():
    return 'All about me!'


@app.route('/courses')
def get_courses():
    return 'All my courses'


@app.route('/courses/create', methods=['GET', 'POST'])
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
        db.session.add(new_course)
        db.session.commit()
        return redirect('/')
    return render_template('create_course.html', form=create_course_form)


@app.route('/courses/<int:course_id>')
def get_course(course_id):
    found_courses = [course for course in courses if course['id'] == course_id]
    if not found_courses:
        abort(404)

    return render_template('course.html', course=found_courses[0])


@app.errorhandler(404)
def handle_404(error):
    return render_template('404.html'), 404


@app.template_filter('datetime')
def datetime_format(value, format="%c"):
    return value.strftime(format)


@app.template_test('new_course')
def is_new(course):
    if 'is_new' not in course:
        return False
    return course['is_new']


if __name__ == '__main__':
    db.create_all()
    app.run()
