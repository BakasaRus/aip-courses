from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


courses = [
    {
        'name': 'Основы программирования на языке Kotlin',
        'desc': 'Курс посвящен изучению языка программирования Kotlin, передовому языку для проектирования различного рода приложений.',
        'img': 'https://cdn.openedu.ru/f1367c/CACHE/images/cover/c820f30eb3223c5142d5fc30c4c1a4383645c49c/f889db722db8aa0a207011ff80bf95f1.png'
    },
    {
        'name': 'Разработка современных мобильных приложений на языке Kotlin',
        'desc': 'Курс посвящен изучению современных способов разработки мобильных приложений на языке Kotlin под ОС Android.',
        'img': 'https://cdn.openedu.ru/f1367c/CACHE/images/cover/318bd6f2d0bbe5b028a4c0d8688ed714684f4cb1/c12c48c9feac6b332fc1c8713ba8922b.png'
    },
    {
        'name': 'Модели и методы аналитической механики',
        'desc': 'В курсе рассматриваются подходы к составлению математических моделей динамических систем и методы их математической обработки.',
        'img': 'https://cdn.openedu.ru/f1367c/CACHE/images/cover/badge_J6JVOr2/ce39a073a96624c22ce5203d473a2969.png'
    },
]


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html', title='Закрытое образование', courses=courses)


@app.route('/about')
def about():
    return 'All about me!'


@app.route('/courses')
def get_courses():
    return 'All my courses'


@app.route('/courses/<int:course_id>')
def get_course(course_id):
    return f'Course #{escape(course_id)}'


if __name__ == '__main__':
    app.run()
