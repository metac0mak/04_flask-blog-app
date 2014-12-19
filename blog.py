
#blog.py -- controller


# imports


from flask 			import Flask, flash, render_template, request, session, \
						   redirect, url_for, g							# from flask module, import listed classes

from functools		import wraps										# used for restricting access 

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


# login required
def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):					# args and 'kw' args as parameters
		if 'logged_in' in session:
			return test(*args, **kwargs)

		else:
			flash('You need to login first . . . ')			# if user not logged in, provide feedback and redirect to login page
			return redirect(url_for('login'))

	return wrap


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


# add posts
@app.route('/add', methods=['POST'])
@login_required
def add():
	title = request.form['title']
	post = request.form['post']

	if not title or not post:
		flash("All fields are required.  Please try again.")
		return redirect(url_for('main'))

	else:
		
		# connect to db
		g.db = connect_db()

		
		# retrieve form contents and insert into db
		g.db.execute('insert into posts (title, post) values (?, ?)', [request.form['title'], request.form['post']])

		# commit changes
		g.db.commit()

		#close connection
		g.db.close()

		# feedback
		flash("Entry successfully posted!")

		# reload main page
		return redirect(url_for('main'))

# main page
@app.route('/main')
@login_required				# @main now calls the @login_required decorator to handle access
def main():

	# connect to db
	g.db = connect_db()
	
	# execute sql
	cur = g.db.execute('SELECT * FROM posts')
	
	# capture sql results to dictionary data type
	# REFRESHER :: Dictionaries are similar to lists, but are unique in that they are key:value pairs.  You can search by 
	# 			   the keys of a dictionary.  
	posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]

	# close connection
	g.db.close()

	return render_template('main.html', posts=posts)


if __name__ == '__main__':
	app.run(debug=True)




