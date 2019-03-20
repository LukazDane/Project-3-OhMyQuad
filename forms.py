from flask_wtf import FlaskForm as Form
from wtforms import TextField, TextAreaField, SubmitField

class WorkoutForm(Form):
  name = TextField("Title")
  description = TextField("steps")
  submit = SubmitField('Create Post')

  







