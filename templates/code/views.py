from flask import Flask, render_template, url_for, request, session, redirect, Blueprint
import bcrypt

app = Flask(__name__)
index_blueprint = Blueprint('index',__name__)

@index_blueprint.route('/login', methods=['POST'])
def login():
	#get database of users
	#find login name in DB
	loginUser = request.form['username']

	if loginUser:
		if bcrypt.hashpw(request.form['pass'].encode('utf-8'), '''db password.encode('utf-8')''') == '''dbpw.encode('utf-8')''':
			session['username'] = request.form['username']
			return redirect(url_for('index'))
		return 'Invalid username/password'

	return 'Invalid username/password'

@index_blueprint.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		#check if username already exists in DB
		if 'hello' == request.form['username']:
			return "That username already exists"

		hashpw = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
		#add this to the DB
		session['username'] = request.form['username']
		return redirect(url_for('index.index'))

	return render_template('/register.html')


@index_blueprint.route('/')
@index_blueprint.route('/index')
def index():
	# add logout feature
	if 'username' in session:
		return 'You are logged in as ' + session['username']
	return render_template('index.html')

@index_blueprint.route('/calendar')
def calendar():
	return 'hi'

# if __name__ == '__main__':
#     app.secret_key = 'mysecret'
#     app.run(debug=True)