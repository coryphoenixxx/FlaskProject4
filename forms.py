from wtforms import StringField, SubmitField, RadioField, IntegerField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

from data import client_times as ctimes


class BookingForm(FlaskForm):
    dow = StringField()
    time = StringField()
    teacher_id = IntegerField()
    name = StringField('Вас зовут:',validators=[DataRequired()])
    phone = StringField('Ваш телефон:', validators=[DataRequired()])
    submit = SubmitField('Записаться на пробный урок')


class RequestForm(FlaskForm):
    goals = RadioField('Какая цель занятий?', choices=[], default='prog')
    times = RadioField('Сколько времени есть?', choices=[(ct, ct) for ct in ctimes], default='1-2')
    name = StringField('Вас зовут:', validators=[DataRequired()])
    phone = StringField('Ваш телефон:', validators=[DataRequired()])
    submit = SubmitField('Найдите мне преподавателя')
