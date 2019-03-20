
from flask import Flask, g
from flask import render_template, flash, redirect, url_for
import models
from forms import WorkoutForm

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'adkjfalj.adflja.dfnasdf.asd'
 

  # Handle requests when the come in (before) and when they complete (after)
@app.before_request
def before_request():
    """Connect to the DB before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


  # The root route will revert back to a simpler version that just returns some text
@app.route('/', methods=['GET', 'POST'])
def index():
  # a form variable representing the SubForm
  form = WorkoutForm()
  #check if the form submission is valid
  if form.validate_on_submit():
  #if it is create a new sub and redirect the user
    models.Workout.create(
        name=form.name.data.strip(), 
        description=form.description.data.strip())

  
  
  #if it isn't send them back to form
  return render_template('new_workout.html', title="New Workout", form=form)

    
    
    
    








if __name__ == '__main__':
  models.initialize()
  try:
     models.User.create_user(

     )
  except ValueError:
      pass
  app.run(debug=DEBUG, port=PORT)
