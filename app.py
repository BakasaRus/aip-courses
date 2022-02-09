from flask import Flask, render_template, abort
from datetime import datetime

app = Flask(__name__)


courses = [
    {
        'name': 'Основы программирования на языке Kotlin',
        'desc': 'Курс посвящен изучению языка программирования Kotlin, передовому языку для проектирования различного рода приложений.',
        'img': 'https://cdn.openedu.ru/f1367c/CACHE/images/cover/c820f30eb3223c5142d5fc30c4c1a4383645c49c/f889db722db8aa0a207011ff80bf95f1.png',
        'is_new': False,
        'start': datetime.fromisoformat('2022-09-23T12:00:00'),
        'end': datetime.fromisoformat('2022-12-23T12:00:00'),
    },
    {
        'name': 'Разработка современных мобильных приложений на языке Kotlin',
        'desc': 'Курс посвящен изучению современных способов разработки мобильных приложений на языке Kotlin под ОС Android.',
        'img': 'https://cdn.openedu.ru/f1367c/CACHE/images/cover/318bd6f2d0bbe5b028a4c0d8688ed714684f4cb1/c12c48c9feac6b332fc1c8713ba8922b.png',
        'is_new': True,
        'start': datetime.now(),
        'end': datetime.now(),
    },
    {
        'name': 'Модели и методы аналитической механики',
        'desc': 'В курсе рассматриваются подходы к составлению математических моделей динамических систем и методы их математической обработки.',
        'img': 'https://cdn.openedu.ru/f1367c/CACHE/images/cover/badge_J6JVOr2/ce39a073a96624c22ce5203d473a2969.png',
        'is_new': True,
        'start': datetime.now(),
        'end': datetime.now(),
    },
    {
        'name': 'Введение в машинное обучение',
        'desc': 'Машинное обучение, его применение и совершенствование — это то, над чем трудятся многие лучшие умы современности.',
        'img': 'https://cdn.openedu.ru/f1367c/CACHE/images/cover/54eda2d1971ba38fd42e9c7afddf54e27f0b34fd/af28f10bf4a4454bfde701ae596c7f3d.png',
        'start': datetime.now(),
        'end': datetime.now(),
    }
]


@app.route('/')
def homepage():  # put application's code here
    return render_template('index.html', title='Закрытое образование', courses=courses)


@app.route('/about')
def about():
    return 'All about me!'


@app.route('/courses')
def get_courses():
    return 'All my courses'


@app.route('/courses/<int:course_id>')
def get_course(course_id):
    if course_id >= len(courses):
        abort(404)
    return render_template('course.html', title='Закрытое образование', course=courses[course_id - 1])


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
    app.run()
