# -*- coding: utf-8 -*-
from app import app,db
from flask import render_template,flash,redirect,url_for, request
from app.forms import LoginForm,RegistrationForm,EditProfileForm
from app.models import User,New
from flask_login import logout_user
from flask_login import current_user, login_user
from flask_login import login_required
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
	news = current_user.followed_posts().all()
	return render_template('index.html',title = 'Home',news=news)
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(name=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(name=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Поздравляю, вы успешно зарегистрировались в системе!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.name = form.name.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Ваши изменения были сохранены.')
		return redirect(url_for('index'))
	elif request.method == 'GET':
		form.name.data = current_user.name
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile',
						   form=form)
@app.route('/follow/<name>')
@login_required
def follow(name):
	user = User.query.filter_by(name=name).first()
	if user is None:
		flash('Пользователь {} не найден.'.format(name))
		return redirect(url_for('index'))
	if user == current_user:
		flash('Вы не можете подписаться сами на себя!')
		return redirect(url_for('user', name=name))
	current_user.follow(user)
	db.session.commit()
	flash('Вы подписались на {}!'.format(name))
	return redirect(url_for('user', name=name))

@app.route('/unfollow/<name>')
@login_required
def unfollow(name):
	user = User.query.filter_by(name=name).first()
	if user is None:
		flash('Пользоватеь {} не найден.'.format(name))
		return redirect(url_for('index'))
	if user == current_user:
		flash('Вы не можете отписаться от себя!')
		return redirect(url_for('user', name=name))
	current_user.unfollow(user)
	db.session.commit()
	flash('Вы отписались от  {}.'.format(name))
	return redirect(url_for('user', name=name))
@app.route('/user/<name>')
@login_required
def user(name):
	user = User.query.filter_by(name=name).first_or_404()
	news = user.followed_posts().all()
	return render_template('user.html', user=user, news=news)