from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
	username = StringField('Имя', validators=[DataRequired()])
	password = PasswordField('Пароль', validators=[DataRequired()])
	remember_me = BooleanField('Запомнить меня')
	submit = SubmitField('Войти в систему')
	
class RegistrationForm(FlaskForm):
	username = StringField('Имя', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Пароль', validators=[DataRequired()])
	password2 = PasswordField(
		'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Зарегистрироваться')

	def validate_username(self, username):
		user = User.query.filter_by(name=username.data).first()
		if user is not None:
			raise ValidationError('Пожалуйста, введите другое имя.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Пожалуйста, введите другую почту.')