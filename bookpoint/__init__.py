from flask import Flask
from sqlalchemy.orm import sessionmaker 
from bookpoint.model.model import Category, Mark, Tag, Base, engine 

app = Flask(__name__) 
Session_db = sessionmaker(bind=engine)
session_db = Session_db()
testvar = 'hi'

import bookpoint.routes #routes imports app, cyclic import, but Flask works like that


