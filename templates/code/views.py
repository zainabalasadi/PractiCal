from flask import render_template, Blueprint
index_blueprint = Blueprint('index',__name__)
@index_blueprint.route('/')
@index_blueprint.route('/index')
def index():
 return render_template("index.html")




from flask import Flask, render_template, url_for, request, session, redirect
import bcrypt

app = Flask(__name__)

@app.route('/login', methods=['POST'])
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

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		#check if username already exists in DB
		if _________ == request.form['username']:
			return "That username already exists"

		hashpw = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
		#add this to the DB
		session['username'] = request.form['username']
		return redirect(url_for('index'))

	return render_template('/register.html')

@app.route('/')
def index():
	if 'username' in session:
		return 'You are logged in as ' + sesion['username']
	return render_template('index.html')

@app.route('/calendar')
def calendar():


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)