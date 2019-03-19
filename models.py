import datetime
#import everything from peewee because we might need it 
from peewee import *


DATABASE = SqliteDatabase('ohmyquad.db')
class user(Model):
  name=
class workout(Model):
  title = CharField(55)
  timestamp = DateTimeField(default=datetime.datetime.now)
  #relate the post to the sub model
  user = ForeignKeyField(Sub, backref="workouts") 

  class Meta:
    database = DATABASE
    order_by = ('-timestamp',)
    
