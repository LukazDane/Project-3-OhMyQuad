import datetime
#import everything from peewee because we might need it 
from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash



DATABASE = SqliteDatabase('ohmyquad.db')



class User(Model):
  name = CharField()
  timestamp = DateTimeField(default=datetime.datetime.now)
  #relate the post to the sub model
  



  class Meta:
    database = DATABASE
    order_by = ('-timestamp',)


class Workout(Model):
  name = CharField()
  timestamp = DateTimeField(default=datetime.datetime.now)
  #relate the post to the sub model
  user = ForeignKeyField(User, backref="workouts") 



  class Meta:
    database = DATABASE
    order_by = ('-timestamp',)


class Exercise(Model):
    name=CharField()
    reps=IntegerField()
    sets=IntegerField()
    description=TextField()
    type=CharField()

    class Meta:
      database = DATABASE


class WorkoutExercise(Model):
    exercise = ForeignKeyField(Exercise) 
    workout = ForeignKeyField(Workout) 

    class Meta:
      database = DATABASE






def initialize():
  DATABASE.connect()
  DATABASE.create_tables([Exercise,Workout,WorkoutExercise,User], safe=True)
  DATABASE.close()
    
