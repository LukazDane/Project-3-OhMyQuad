from flask_wtf import FlaskForm as Form
from wtforms import TextField, TextAreaField, SubmitField



class PostForm(Form):
  user = TextField("By:")
  title = TextField("Title")
  text = TextAreaField("Content")
  submit = SubmitField('Create Post')