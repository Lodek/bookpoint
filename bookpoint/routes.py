from bookpoint import app
from bookpoint.controllers import readingq, bookpoint, sessions


#Bookpoint Routes
@app.route('/')
def bookpoint_home():
    return bookpoint.home()

@app.route('/orghome')
def bookpoint_orghome():
    return bookpoint.orghome()

@app.route('/new')
def bookpoint_new():
    return bookpoint.new()

@app.route('/create')
def bookpoint_create():
    return bookpoint.create()


#Sessions routes
@app.route('/sessions/')
def sessions_home():
    return sessions.home()

@app.route('/sessions/orghome')
def sessions_orghome():
    return sessions.orghome()

@app.route('/sessions/new')
def sessions_new():
    return sessions.new()

@app.route('/sessions/create')
def sessions_create():
    return sessions.create()


#Reading Queue routes
@app.route('/readingq/')
def readingq_home():
    return session.home()

@app.route('/readingq/orghome')
def readingq_orghome():
    return readingq.orghome()

@app.route('/readingq/new')
def readingq_new():
    return readingq.new()

@app.route('/readingq/create')
def readingq_create():
    return readingq.create()

