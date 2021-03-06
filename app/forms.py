from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField  
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo,Length
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
class EditProfileForm(FlaskForm):
	name = StringField('Имя', validators=[DataRequired()])
	about_me = TextAreaField('Обо мне:', validators=[Length(min=0, max=140)])
	male = BooleanField('М')
	female = BooleanField('Ж')
	submit = SubmitField('Сохранить')

class PostForm(FlaskForm):
	post = TextAreaField('Напишите что-нибудь', validators=[
		DataRequired(), Length(min=1, max=140)])
	submit = SubmitField('Отправить')
