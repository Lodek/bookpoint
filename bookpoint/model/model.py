from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Table, Date
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()
engine = create_engine('sqlite:///bookpoint/model/bookpoint.db', echo=True)

tag_mark_tb = Table('mark_tag', Base.metadata, Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True), Column('mark_id', Integer, ForeignKey('marks.id'), primary_key=True))

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key = True)
    name = Column(String)
    mark = relationship('Mark', back_populates='category')

    
class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key = True)
    name = Column(String)
    marks = relationship('Mark', secondary=tag_mark_tb, back_populates='tags')
    
class Mark(Base):
    __tablename__ = 'marks'

    id = Column(Integer, primary_key = True)
    url = Column(String)
    title = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='mark')
    notes = Column(String)
    tags = relationship("Tag", secondary=tag_mark_tb, back_populates='marks')

    date_added = Column(Date, default=datetime.date.today())
    tags_str = ''
    
def create_all():
    Base.metadata.create_all(engine)

