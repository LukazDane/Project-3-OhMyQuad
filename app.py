from flask import render_template, flash, redirect, url_for
from forms import SubForm, PostForm, CommentForm
#This import makes our connection to the models
import models

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'adkjfalj.adflja.dfnasdf.asd'












if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)
