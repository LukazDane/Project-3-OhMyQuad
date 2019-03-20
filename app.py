from flask import Flask, g
from flask import render_template, flash, redirect, url_for, session

from forms import WorkoutForm
import models


DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'dev'
 

  # Handle requests when the come in (before) and when they complete (after)
# @app.before_request
# def before_request():
#     # """Connect to the DB before each request."""
#     g.db = models.DATABASE
#     g.db.connect()

# @app.after_request
# def after_request():
#     # """Close the database connection after each request."""
#     g.db.close()
#     return response

@app.route("/")
def index(name=None):
    return render_template('layout.html',title="Dashboard", name=name)

@app.route("/profile")
def profile(name=None):
    return render_template('profile.html',title="Dashboard", name=name)

@app.route("/about")
def about(name=None):
    return render_template('about.html',title="About Us", name=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))
  # The root route will revert back to a simpler version that just returns some text


  # ...
    
    
    
    








if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)
