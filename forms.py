from flask_wtf import FlaskForm as Form

from wtforms import TextField, TextAreaField, SubmitField, StringField, PasswordField, IntegerField

from wtforms.validators import (DataRequired, Regexp, ValidationError, Email, Length, EqualTo, NumberRange)

from flask_login import UserMixin

from flask_bcrypt import generate_password_hash

from models import User

def name_exists(form, field):
    if User.select().where(User.username == field.data). exists():
        raise ValidationError("User with this username already exists!")

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("Someone with this email is already in the DB")


class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, numbers, and underscores only")
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators = [
            DataRequired(),
            Length(min=2),
            EqualTo('Password2', message='Passwords must match')
        ])
    Password2 = PasswordField(
        'Confirm Password',
        validators = [DataRequired()]
    )
    name = StringField(
        'Name',
        validators = [
            DataRequired()
        ])
    height = IntegerField(
        'Height in Inches',
        validators=[
            NumberRange(min= 36, max=99, message='Incorrect input. Height must be greater than 36 inches and less than 99 inches')
        ]
        )
    weight = IntegerField(
        'Weight in Pounds',
        validators = [
            NumberRange(min= None, max=999, message='Please input a weight less than 1000 pounds')
        ]
        )
    goal = TextAreaField(
        'Current Goal',
        validators = [
            DataRequired()
        ])

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired() ])


class WorkoutForm(Form):
    # name = TextField("By:")
    name = TextField("Title")
    description = TextAreaField("Content")
    submit = SubmitField('Create Workout')


class EditWorkoutForm(Form):
    name = TextField("By:")
    title = TextField("Title")
    description = TextAreaField("Content")
    submit = SubmitField('Edit Workout')