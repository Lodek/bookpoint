from bookpoint.model.model import Category, Mark, Tag, Base, engine, create_all
from sqlalchemy.orm import sessionmaker

Session_db = sessionmaker(bind=engine)
session_db = Session_db()

create_all()

session_db.add_all([Category(name='readingq')])
session_tag = Tag(name='session')

mark = Mark(url='url', title='title', category_id=1, notes='notes')
mark2 = Mark(url='url', title='title', category_id=1, notes='notes')


mark.tags.append(session_tag)
mark.tags.append(Tag(name='python'))
mark2.tags.append(session_tag)

session_db.add(mark)
session_db.add(mark2)

session_db.commit()

mark_list = session_tag.marks

for mark in mark_list:
    print(mark.id)
