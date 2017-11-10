from bookpoint.model.model import Category, Mark, Tag, Base, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

mark = session.query(Mark)

mark_dict = {}
for category in session.query(Category.name).all():
    marks_list = []
    for mark in session.query(Mark).all():
        tags = ':'
        for tag in mark.tags:
            tags += '{}:'.format(tag.name)
        marks_list.append([mark,tags])
    mark_dict[category] = marks_list

for category, marks in mark_dict.items():
    print(category)
    for mark in marks:
        print(mark[0].url, mark[0].title, mark[0].date_added, mark[1])
