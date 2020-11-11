# -*- coding: utf-8 -*- 
from flask import render_template, flash, redirect, url_for, request
from app import app, db, errors, logger
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user,  login_required
from app.models import User
from werkzeug.urls import url_parse
from app.forms import RegistrationForm, EditProfileForm, SearchForm
from datetime import datetime
from guess_language import guess_language
from flask import jsonify
from app.translate import translate
from googleapiclient.discovery import build
import pprint

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	user = User.query.filter_by(username='123').first_or_404()
	posts = user.posts
	
	for post in posts:
		language = guess_language(post.body)
		if language == 'UNKNOWN' or len(language) > 5:
			language = ''
		post.language=language	
					
	return render_template('index.html', title='Home', posts=posts)

@app.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['dest_language'])})
	
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile',
						   form=form)

	
@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
	
@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	posts = current_user.posts
	return render_template('user.html', user=user, posts=posts)	

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		
#		if (not next_page):
#			print('1 not next page')
#			
#			if (url_parse(next_page).netloc != ''):
#				print('2 '+url_parse(next_page).netloc)
		
		if current_user.is_authenticated:
			if not next_page or url_parse(next_page).netloc != '':
				next_page = url_for('index')	
			return redirect(next_page)

	return render_template('login.html', title='Sign In', form=form)
	
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/geterror')
def geterror():
	er = User(username='123',email='123@gmail.com')
	db.session.add(er)
	db.commit()
	return redirect(url_for('index'))
	#return redirect(url_for('geterror'))
	
@app.route('/google_search', methods=['GET', 'POST'])
def google_search():
	form = SearchForm()	
	res=''
	if form.validate_on_submit():
		flash('Searching: ' + form.search_field.data)
		service = build("customsearch", "v1",developerKey=app.config['GOOGLE_DEV_KEY'])
		res = service.cse().list(
			q=form.search_field.data,
			cx='017576662512468239146:omuauf_lfve',
			).execute()
		#results = pprint.pprint(res)
		
	return render_template('google_search/google_search.html', title='Search', form=form, res=res)
	#return redirect(url_for('google_search'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)