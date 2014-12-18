
#blog.py -- controller


# imports


from flask 			import Flask, render_template, request, session, \
						   redirect, url_for, g							# from flask module, import listed classes

import sqlite3															# import sqlite3 module
import os																# use for secret key generation
# ------


# configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'

#SECRET_KEY = 'hard_to_guess'
# Make this key impossible to guess
SECRET_KEY = os.urandom(24)

app = Flask(__name__)


# pulls in app configuration by looking for UPPERCASE variables		--> the DATABASE variable . . . 
app.config.from_object(__name__)


# function used for connecting to database
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])


# add necessary routes

# login
@app.route('/')		
def login():
	return render_template('login.html')

# main page
@app.route('/main')
def main():
	return render_template('main.html')


if __name__ == '__main__':
	app.run(debug=True)




