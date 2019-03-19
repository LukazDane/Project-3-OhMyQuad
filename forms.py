from flask_wtf import FlaskForm as Form
from wtforms import TextField, TextAreaField, SubmitField



class WorkoutForm(Form):
  user = TextField("By:")
  title = TextField("Title")
  text = TextAreaField("Content")
  submit = SubmitField('Create Workout')