from bookpoint.model.model import Category, Mark, Tag, Base, engine
from flask import Flask
from sqlalchemy.orm import sessionmaker

app = Flask(__name__) 

Session = sessionmaker(bind=engine)
session = Session()

import bookpoint.routes
