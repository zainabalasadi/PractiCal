import bcrypt
from flask import Flask, render_template, url_for, request, session, redirect, Blueprint, flash
from flask_login import login_user, logout_user, login_required, current_user
import dialogflow_v2
from google.api_core.exceptions import InvalidArgument
import requests

from templates.code.PractiCalManager import PractiCalManager
from templates.code.User import User

DIALOGFLOW_PROJECT_ID = 'practical-proueq'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
GOOGLE_APPLICATION_CREDENTIALS = 'googlekey.json'
sessionClient = dialogflow_v2.SessionsClient()

index_blueprint = Blueprint('index', __name__)

PCM = PractiCalManager('practiCal_db', 'localhost', 'admin', 'password')

@index_blueprint.route('/', methods=['GET', 'POST'])
@index_blueprint.route('/index', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')

		user = PCM.loginUser(email,
                    bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))

		if not user:
			flash('Please check your login details and try again.')
			return redirect(url_for('index.index'))

		login_user(user, remember=True)
		return redirect(url_for('index.calendar'))

	return render_template('/index.html')

@index_blueprint.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index.index'))

@index_blueprint.route('/forgot', methods=['GET', 'POST'])
def forgot():
	if request.method == 'POST':
		
		email = request.form.get('email')
		# TODO insert code to send reset password email
		flash('Password reset has been sent to your email.')
		return redirect(url_for('index.index'))

	return render_template('/forgot.html')

@index_blueprint.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		
		email = request.form.get('email')
		firstName = request.form.get('firstName')
		lastName = request.form.get('lastName')
		password = request.form.get('password')
		
		# hash user password and then add user to database
		hashpw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

		if PCM.createUser(firstName, lastName, email, hashpw) is False:
			flash('Email address already exists.')
			return redirect(url_for('index.register'))

		return redirect(url_for('index.index'))

	return render_template('/register.html')

@index_blueprint.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
	return render_template('/calendar.html', name=current_user.getFirstName())

post_blueprint = Blueprint('post',__name__)
@post_blueprint.route("/getIntent", methods=['POST'])
def getIntent():
    textMsg = request.form['message']

    SESSION_ID = current_user.getId() #needs to be replaced with the logged in users id
    session = sessionClient.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

    textInput = dialogflow_v2.types.TextInput(text="Make an event for today at 10pm", language_code=DIALOGFLOW_LANGUAGE_CODE)
    queryInput = dialogflow_v2.types.QueryInput(text=textInput)

    response = sessionClient.detect_intent(session=session, query_input=queryInput)
    if (response.query_result.intent.display_name == "Event scheduling"):
        return jsonify({"date" : response.query_result.parameters.fields["date"].string_value,
                        "timeStart" : response.query_result.parameters.fields["timeStart"].string_value,
                        "timeEnd" : response.query_result.parameters.fields["timeEnd"].string_value
        })
