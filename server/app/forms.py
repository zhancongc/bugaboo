"""
Project     : bugaboo
Filename    : forms.py
Author      : zhancongc
Description : 表单管理
"""

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SelectField, FileField, IntegerField, PasswordField
from wtforms.validators import DataRequired


class GodLoginForm(FlaskForm):
    """
    登陆表单
    """
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])



