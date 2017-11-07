from bookpoint.model.model import Category, Mark, Tag, Base, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

mark = Mark(url='url', title='title', notes='note')

cat = Category(name='cool_cat')

mark.category = cat

mark.tags = [Tag(name='python'), Tag(name='memes')]

