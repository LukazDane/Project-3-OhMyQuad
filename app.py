from flask import Flask, g
import models


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
def after_request():
    """Close the database connection after each request."""
    g.db.close()
    return response


  # The root route will revert back to a simpler version that just returns some text
@app.route('/')
def index():
    return 'Integrating models with this route'

  # ...
    
    
    
    








if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)
