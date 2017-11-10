from bookpoint import app
from bookpoint.controllers import readingq, mark, session

@app.route('/')
def home():
    return mark.home()
