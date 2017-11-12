from bookpoint.model.model import Category, Mark, Tag, Base, engine
from flask import Flask
from sqlalchemy.orm import sessionmaker

app = Flask(__name__) 

Session_db = sessionmaker(bind=engine)
session_db = Session_db()

import bookpoint.routes
