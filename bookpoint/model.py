from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import Database 
import datetime
import regexes
import lib


Base = declarative_base()

tag_mark_tb = Table('mark_tag', Base.metadata, Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True), Column('mark_id', Integer, ForeignKey('marks.id'), primary_key=True))

db_session = Database().session

class Category(Base):
    
    """ SQL Alchemy mapper class for the catogories table in the database. The columns of the table are class-wide declaration. 
    Category has a one to many relationship with Mark. Class contain methods for returning the correct Category object from a string
    matching the expected org file format."""
    
    __tablename__ = 'categories'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    marks = relationship('Mark', back_populates='category')

    
    def get_from_raw(self,category_raw):
        """ Method that returns a Category object matching the category that is on the list received as paramater.
        The list contains the category name and its marks (in org-mode markup)
        sample input ['* Category_Name', '** [[mark_url][mark_title]]'...]"""
        name = re.search(lib.regexes['categories'], category_raw[0]).group(1)
        category = db.q_category().filter(Category.name == name).first()
        if not category:
            category = Category(name=name)
        category.marks_raw = raw_category[1:]
        return category
        
            
class Mark(Base):

    """ Mapper class for the marks table in the database. Table Columns are class wide declarations.
    Mark has a many to one relationship with Category,
    a many to many relationship with Tag,
    a many to one relationship with Note """

    __tablename__ = 'marks'
    id = Column(Integer, primary_key = True)
    url = Column(String)
    title = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='marks')
    notes = relationship('Note', back_populates='mark')
    tags = relationship("Tag", secondary=tag_mark_tb, back_populates='marks')
    date = Column(Date, default=datetime.date.today())

    
    def add_mark(self,url):
        db_session.add(Mark(url=url, title=self.get_title(url)))
        db_session.commit()
        return
    
    def get_from_raw(mark_raw,db):
        """ Method that receives the body of a Mark as a list in raw form (org-mode markup). 
        The received list is processed and a mark object is returned matching the URL from the list. 
        The object may be a new object (in case of a new mark) or one that already exists in the db.
        Finally, the new mark object will contain in its instance a tag_raw and a notes_raw attribute. """
        regex = lib.regexes['marks']
        match = re.search(regex,mark_raw[0])
        url = match.group(1)
        tags = match.group(2)
        mark = db.q_mark().filter(Mark.url == url).first()
        if not mark:
            mark = Mark(url=url, title=lib.get_title(url))
        mark.tags_raw = tags
        mark.notes_raw = mark_raw[1:]
        return mark

    def _get_title(self,url):
        """ Given an url the function returns the title of the page, if it fails to connect or if the website doesn't exist returns the url."""
        # Discard exception for when the url is not valid or whatever
        try:
            obj=requests.get(url)
            title=re.search('<title>(.*?)<\/title>',obj.text).group(1).replace('[', '|').replace(']','|')
        except BaseException:
            title=url
        return title


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    marks = relationship('Mark', secondary=tag_mark_tb, back_populates='tags')

    def get_from_raw(self,tag_raw,db):
        tag = db.q_tag().filter(Tag.name == tag_raw).first()
        if not tag:
            tag = Tag(name=tag_raw)
        return tag
    

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key = True)
    body = Column(String)
    mark_id = Column(Integer, ForeignKey('marks.id'))
    mark = relationship('Mark', back_populates='notes')
