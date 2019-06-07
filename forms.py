from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('用户名已经存在，请重新选择一个用户名')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('邮箱地址已经存在，请重新选择一个邮箱地址')


class LoginForm(FlaskForm):
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('用户名',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('邮件地址',
                            validators=[DataRequired(), Email()])
    picture = FileField('上传头像图片',
                            validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('更新')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('用户名已经存在，请重新选择一个用户名')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('邮箱地址已经存在，请重新选择一个邮箱地址')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
