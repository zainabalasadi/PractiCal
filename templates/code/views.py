from flask import Flask, render_template, url_for, request, session, redirect, Blueprint, flash
import bcrypt

from templates.code.PractiCalManager import PractiCalManager
from templates.code.User import User


index_blueprint = Blueprint('index', __name__)

pcm = PractiCalManager()

@index_blueprint.route('/')
@index_blueprint.route('/index')
def index():
	# if 'username' in session:
	# 	return redirect(url_for('index.calendar'))

	# get database of users
	# find login name in DB
	# loginUser = request.form['username']

	# if loginUser:
	# 	if bcrypt.hashpw(request.form['pass'].encode('utf-8'), '''db password.encode('utf-8')''') == '''dbpw.encode('utf-8')''':
	# 		session['username'] = request.form['username']
	# 		return redirect(url_for('index'))
	# 	return 'Invalid username/password'

	# return 'Invalid username/password'
	return render_template('index.html')

@index_blueprint.route('/logout')
def logout():
	return 'Logout'

@index_blueprint.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		
		email = request.form.get('email')
		firstName = request.form.get('firstName')
		lastName = request.form.get('lastName')
		password = request.form.get('password')
		
		# hash user password and then add user to database
		hashpw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

		# check if email already exists
		if pcm.createUser(firstName, lastName, email, hashpw) is False:
			flash('Email address already exists')
			return redirect(url_for('index.register'))

		return redirect(url_for('index.index'))

	return render_template('/register.html')

@index_blueprint.route('/calendar', methods=['GET', 'POST'])
def calendar():
	return render_template('/calendar.html', user=session['username'])