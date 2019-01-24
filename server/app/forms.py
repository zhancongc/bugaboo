"""
Project     : bugaboo
Filename    : forms.py
Author      : zhancongc
Description : 表单管理
"""

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SelectField, FileField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class GodLoginForm(FlaskForm):
    """
    登陆表单
    """
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField()


class ExchangeAwardForm(FlaskForm):
    """
    登陆表单
    """
    awardrecord_token = StringField('awardrecord_token', validators=[DataRequired()])
    exchange_token = PasswordField('exchange_token', validators=[DataRequired()])
    submit = SubmitField()




