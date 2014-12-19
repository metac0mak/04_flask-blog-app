
#blog.py -- controller


# imports


from flask 			import Flask, flash, render_template, request, session, \
						   redirect, url_for, g							# from flask module, import listed classes

import sqlite3															# import sqlite3 module
import os																# use for secret key generation
# ------


# configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'

SECRET_KEY = 'hard_to_guess'
# Make this key impossible to guess
# SECRET_KEY = os.urandom(24)

app = Flask(__name__)


# pulls in app configuration by looking for UPPERCASE variables		--> the DATABASE variable . . . 
app.config.from_object(__name__)


# function used for connecting to database
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])


# add necessary routes

# login
@app.route('/', methods = ['GET', 'POST'])		
def login():
	error = None
	if request.method == 'POST':
		if 	request.form['username'] != app.config['USERNAME'] or \
			request.form['password'] != app.config['PASSWORD']:

			error = 'Invalid Credentials. Please try again.'

		else:
			flash('You were logged in')
			session['logged_in'] = True				# user is logged in
			return redirect(url_for('main'))		# redirect_for() - "generates an enpoint for the provided method."

	return render_template('login.html', error = error )


# logout
@app.route('/logout')
def logout():
	session.pop('logged_in', None)			# pop method - "resets the session key to the default value"
	flash('You were logged out')
	return redirect(url_for('login'))		# user redirected back to login page

# main page
@app.route('/main')
def main():
	return render_template('main.html')


if __name__ == '__main__':
	app.run(debug=True)




