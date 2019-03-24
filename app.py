from flask import Flask, g
from flask import render_template, flash, redirect, url_for, session, request, abort 
from flask import make_response as response
from forms import WorkoutForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash

import forms 
import models

DEBUG = True
PORT = 9000

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
        return None

# Handle requests when the come in (before) and when they complete (after)
@app.before_request
def before_request():
    # """Connect to the DB before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    # """Close the database connection after each request."""
    g.db.close()
    return response

## =======================================================
## ROOT ROUTE
## =======================================================

@app.route("/")
def index(name=None):
    if 'auth_token' in session:
    
        return redirect(url_for('profile'))
    else: 
        return render_template('landing.html',title="Dashboard", name=name)


## =======================================================
## DELETE WORKOUT ROUTE
## =======================================================

@app.route("/profile/<workoutid>")
@login_required
def delete_workout(workoutid):
    # form = forms.WorkoutForm()
    workout = models.Workout.get(workoutid)
    workout.delete_instance()
    # workouts = models.Workout.select().where(models.Workout.user == current_user.id)
    return redirect(url_for('profile'))
    # return render_template("profile.html", user=current_user, form=form, workouts=workouts)

## =======================================================
## EDIT WORKOUT ROUTE
## =======================================================

@app.route("/editworkout/<workoutid>", methods=["GET", "POST"])
@login_required
def edit_workout(workoutid):
    workout = models.Workout.get(models.Workout.id == workoutid)
    form = forms.WorkoutForm()
    if form.validate_on_submit():
        workout.name = form.name.data
        workout.description = form.description.data
        workout.save()
        workouts = models.Workout.select().where(models.Workout.user == current_user.id)
        return render_template("profile.html", user=current_user, form=form, workouts=workouts)
    
    form.name.data = workout.name
    form.description.data = workout.description
    return render_template("edit_workout.html", user=current_user, form=form)

@app.route("/addworkout", methods=['GET', 'POST'])
@login_required
def add_workout():
    form = forms.WorkoutForm()
    workouts = models.Workout.select().where(models.Workout.user == current_user.id)
    print('in profile')
    if form.validate_on_submit():
        models.Workout.create(
        name=form.name.data,
        description=form.description.data.strip(), 
        user = current_user.id)
        return render_template("profile.html", user=current_user, form=form, workouts=workouts)

    #form.name.data = workout.name
    #form.description.data = workout.description
    return render_template("add_workout.html", user=current_user, form=form, workouts=workouts)

@app.route("/profile/")
@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = forms.WorkoutForm()
    workouts = models.Workout.select().where(models.Workout.user == current_user.id)
    
    if form.validate_on_submit():
        models.Workout.create(
        name=form.name.data.strip(),
        description=form.description.data.strip(), 
        user = current_user.id)
        return render_template("profile.html", user=current_user, form=form, workouts=workouts)
    return render_template("profile.html", user=current_user, form=form, workouts=workouts)


## =======================================================
## EDIT PROFILE ROUTE
## =======================================================

@app.route('/editProfile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form= forms.UpdateUserForm()
    user = models.User.get(current_user.id)
    if form.validate_on_submit():
        user.height = form.height.data
        user.weight = form.weight.data
        user.goal = form.goal.data
        user.save()
        flash('Your Profile has been updated.') # redirects the user back to the profile page after the form is submitted
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', form = form)
    # return render_template('profile.html',title="Dashboard", name=name)


## =======================================================
## REGISTER ROUTE
## =======================================================


@app.route('/register', methods = ('GET', 'POST'))
def register():
    form = forms.RegisterForm() # importing the RegisterFrom from forms.py
    if form.validate_on_submit(): #if the data in the form is valid,  then we are gonna create a user
        flash("Successful Signup!", 'Sucess')
        models.User.create_user(  # calling the create_user function from the user model and passing in the form data
            username = form.username.data,
            email = form.email.data,
            password = form.password.data,
            name = form.name.data,
            height = form.height.data,
            weight = form.weight.data,
            goal = form.goal.data
            )
        return redirect('/login') # once the submissin is succesful, user is redirected to the index function which routes back to the home page
    return render_template('register.html', form=form)


## =======================================================
## LOGIN ROUTE
## =======================================================

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data) # comparing the user email in the database to the one put in the form
        except models.DoesNotExist:
            flash("your email or password doesn't exist in our database")
        else:   # using the check_password_hash method bc we hashed the user's password when they registered. comparing the user's password in the database to the password put into the form
            if check_password_hash(user.password, form.password.data):
                ## creates session
                login_user(user) # this method comes from the flask_login package
                flash("You've been logged in", "success")
                return redirect('/profile')
            else:
                flash("your email or password doesn't match", "error")
    
    return render_template('login.html', form=form)

## =======================================================
## LOGOUT ROUTE
## =======================================================

@app.route('/logout')
@login_required # defines whatever routes and functions are avail when the user is login in aka "Protects the routes"
def logout():
    logout_user() # method that is defined by flask_login
    flash("You've been logged out", "success") , # second argument gives the flash message a class of sucess 
    return redirect(url_for('index'))




@app.route("/about")
def about(name=None):
    return render_template('about.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
# @app.route('/profile',methods=['GET', 'POST'])
# @app.route('/profile/')
# @app.route('/profile/<workoutid>')
# def user():
#     form = forms.WorkoutForm()
#     workouts = models.Workout.select()
    # if form.validate_on_submit():
#         models.Workout.create(
#         name=form.name.data.strip(),
#         description=form.description.data.strip(), 
#         user = current_user.id)
    #     return render_template("profile.html", user=current_user, form=form, workouts=workouts)
    # return render_template("profile.html", user=current_user, form=form, workouts=workouts)
    # user_id = int(user)
    # user= models.User.get(models.User.id == user_id)
    # workouts = user.workouts
        
   
    
    # Define the form for Posts
    
    # 

#       flash("New post created")
    #   return redirect("/user/{}".format(workout_id))
    # return render_template(".html", sub=sub, form=form , posts=posts)


    
    
    
    












if __name__ == '__main__':
    models.initialize()

    try:
        models.Exercise.create_exercise(
        name='Lat Pulldown',
        description="4 sets, 15 Reps (1 warm-up set of 15 reps, 3 working sets of 15 reps)",
        type='Lats'
        )

        models.Exercise.create_exercise(
        name='Seated Cable Rows',
        description="4 sets, 15 Reps (1 warm-up set of 15 reps, 3 working sets of 15 reps)",
        type='Lats',
       
        ),
        models.Exercise.create_exercise(
        name='Underhand Cable Pulldowns',
        description="3 sets, 10-12 Reps",
        type='Lats',
       
        ),
        models.Exercise.create_exercise(
        name='Barbell Squat',
        description="4 sets, 4-6 reps",
        type='Lats',
       
        ),
        models.Exercise.create_exercise(
        name='Dumbbell Lunges. ',
        description="4 sets, 12 reps each leg",
        type='Legs',
       
        ),
        models.Exercise.create_exercise(
        name='Leg Press. ',
        description="3 sets, 12-15 reps",
          type='Legs',
       
        ),
        models.Exercise.create_exercise(
        name='Underhand Cable Pulldowns',
        description="3 sets, 10-12 Reps",
        type='Legs',
       
        ),
        models.Exercise.create_exercise(
        name='Close-Grip Bench Press',
        description="4 sets, 6, 6, 8, 10 reps (60-90 seconds rest)",
        type='Lats',
       
        ),
        models.Exercise.create_exercise(
        name='Seated Dumbell Press',
        description="3 sets, 8, 10, 12 reps (60 seconds rest)",
        type='Triceps',
       
        ),
        models.Exercise.create_exercise(
        name='V-Bar Pulldown',
        description="2 sets, 10, 12 reps (60 seconds rest)",
        type='Triceps',
       
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, port=PORT)
