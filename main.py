from bookpoint.model.model import Category, Mark, Tag, Base, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

for name in session.query(Mark):
    print(name.date_added)
    
