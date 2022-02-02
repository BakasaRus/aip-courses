from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


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
