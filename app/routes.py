# -*- coding: utf-8 -*-
from app import app
from flask import render_template
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	user = {'name':'Андрей'}
	news = [
        {
            'author': {'name': 'Никита','gender':'male'},
            'body': 'Успешно сдал экзамен!'
             

        },
        {
            'author': {'name': 'Саша','gender':'male'},
            'body': 'Скоро новый семестр=/'
            
        }, 
        {
            'author': {'name': 'Марина','gender':'female'},
            'body': 'Все приходите в дк 22 марта!'
        }
    ]
	return render_template('index.html',title = 'Home',user=user,news=news)
@app.route('/login')
def login():
	form = LoginForm()
	return render_template('login.html', title='Sign In', form=form)