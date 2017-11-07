from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship

Base = declarative_base()
engine = create_engine('sqlite:///bookpoint/model/bookpoint.db', echo=True)

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key = True)
    name = Column(String)
    mark = relationship('Mark', back_populates='category')

    
class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key = True)
    name = Column(String)

    
class Mark(Base):
    __tablename__ = 'marks'

    id = Column(Integer, primary_key = True)
    url = Column(String)
    title = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='mark')
    notes = Column(String)
    tags = relationship("Tag", secondary=Table('mark_tag', Base.metadata, Column('mark_id', Integer, ForeignKey('marks.id')), Column('tag_id', Integer, ForeignKey('tags.id'))))
#    date_added = 
    
Base.metadata.create_all(engine)
