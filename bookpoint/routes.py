from bookpoint import app
from bookpoint.controllers import readingq, bookpoint, session

@app.route('/')
def bookpoint_home():
    return bookpoint.home()

@app.route('/org')
def bookpoint_orghome():
    return bookpoint.orghome()

@app.route('/new')
def bookpoint_new():
    return bookpoint.new()

