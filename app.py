from flask import Flask, g
from flask import render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash

import forms 
import models


DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'elsdhfsdlfdsjfkljdslfhjlds'

login_manager = LoginManager() # init instance ofhte LoginManager class
login_manager.init_app(app) ## sets up our login for the app
login_manager.login_view = 'login' # setting default login view as the login function

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return none

# Handle requests when the come in (before) and when they complete (after)
@app.before_request
def before_request():
    # """Connect to the DB before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    # """Close the database connection after each request."""
    g.db.close()
    return response

@app.route("/")
def index(name=None):
    return render_template('layout.html',title="Dashboard", name=name)


@app.route('/register', methods = ('GET', 'POST'))
def register():
    form = forms.RegisterForm() # importing the RegisterFrom from forms.py
    if form.validate_on_submit(): #if the data in the form is valid,  then we are gonna create a user
        flash("Successful Signup!", 'Sucess')
        models.User.create_user(  # calling the create_user function from the user model and passing in the form data
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
            )
        return redirect(url_for('index')) # once the submissin is succesful, user is redirected to the index function which routes back to the home page
    return render_template('register.html', form=form)

@app.route("/about")
def about():
    return 'About Page!'

@app.route("/login")
def login():
    return 'Login Page!'


  # The root route will revert back to a simpler version that just returns some text


  # ...
    
    
    
    








if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)
