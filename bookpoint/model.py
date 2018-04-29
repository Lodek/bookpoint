from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import logging, requests, datetime, re 
import utils 

logger = logging.getLogger('bookpoint.model')

Base = declarative_base()

tag_mark_tb = Table('mark_tag', Base.metadata, Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True), Column('mark_id', Integer, ForeignKey('marks.id'), primary_key=True))


class Category(Base):
    
    """ SQL Alchemy mapper class for the categories table in the database. The columns of the table are class-wide declaration. 
    Category has a one to many relationship with Mark. Class contain methods for returning the correct Category object from a string
    matching the expected org file format."""
    
    __tablename__ = 'categories'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    marks = relationship('Mark', back_populates='category')

    @classmethod
    def get_from_raw(cls, category_raw, db):
        """ Method returns a Category object matching the category_raw string.
        Sample category_raw >> '* Category_Name' 
        Contract - category_raw must be a valid string """
        name = re.search(utils.regexes['categories'], category_raw).group(1)
        category = db.query(cls).filter(cls.name==name).first()
        if not category:
            category = cls(name=name)
        logger.debug('Returning category named {}'.format(category.name))
        return category


class Mark(Base):

    """ Mapper class for the marks table in the database. Table Columns are class wide declarations.
    Mark has a many to one relationship with Category and a many to many relationship with Tag """

    __tablename__ = 'marks'
    id = Column(Integer, primary_key = True)
    url = Column(String)
    title = Column(String)
    notes = Column(String)
    date = Column(Date, default=datetime.date.today())
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='marks')
    tags = relationship("Tag", secondary=tag_mark_tb, back_populates='marks')

    @classmethod
    def get_from_raw(cls, mark_raw, db):
        """ Method that receives the first line of a Mark as a string and returns the matching mark object
        sample mark_raw >>> '** [[mark_url]] 
        Contract - mark_raw must be a valid mark string"""
        match = re.search(utils.regexes['marks'], mark_raw)
        url = match.group(1)
        mark = db.query(cls).filter(cls.url==url).first()
        if not mark:
            mark = Mark(url=url, title=cls._get_title(url))
        logger.debug('Returning mark {}'.format(mark.url))
        return mark

    @staticmethod
    def _get_title(url):
        """ Given an url the function returns the title of the page, if it fails to connect or if the website doesn't exist returns the url."""
        try:
            obj=requests.get(url)
            title=re.search('<title>(.*?)<\/title>',obj.text).group(1).replace('[', '|').replace(']','|')
        except BaseException:
            title=url
            logger.debug('Could not get title for {}'.format(url))
        return title


class Tag(Base):

    """ Mapper class for tags table in database. tags has a many to many relationship with mark """

    __tablename__ = 'tags'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    marks = relationship('Mark', secondary=tag_mark_tb, back_populates='tags')

    @classmethod
    def get_from_raw(cls, tags_raw, db):
        """ Given a string of tags returns a list of Tag objects. 
        Ex input >>> ':tag1:tag2:tag3: 
                 >>> ''
        Contract - tags_raw must be a valid tag string """
        if tags_raw == '' or tags_raw == '::':
            logger.debug('Returning 0 tag objects')
            return []
        tags_raw = tags_raw[1:-1].split(':')
        tags = []
        for tag_raw in tags_raw:
            tag = db.query(cls).filter(cls.name==tag_raw).first()
            if not tag:
                tag = cls(name=tag_raw)
            tags.append(tag)
        lg = [tag.name for tag in tags]
        logger.debug('Returning {} as tags'.format(lg))
        return tags
