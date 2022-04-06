from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, TextAreaField, URLField, BooleanField, DateTimeLocalField, EmailField, PasswordField
from wtforms.validators import DataRequired, URL


csrf = CSRFProtect()


class CreateCourseForm(FlaskForm):
    name = StringField(label='Название курса', validators=[DataRequired()])
    description = TextAreaField(label='Описание', validators=[DataRequired()])
    cover = URLField(label='Ссылка на обложку', validators=[DataRequired(), URL()])
    is_new = BooleanField(label='Новый курс')
    date_start = DateTimeLocalField(label='Дата начала', format='%Y-%m-%dT%H:%M')
    date_end = DateTimeLocalField(label='Дата окончания', format='%Y-%m-%dT%H:%M')


class LoginForm(FlaskForm):
    email = EmailField(label='Электронная почта', validators=[DataRequired()])
    password = PasswordField(label='Пароль', validators=[DataRequired()])
    remember_me = BooleanField(label='Запомнить меня')
