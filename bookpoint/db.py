from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from model import Category, Mark, Note, Tag
import logging

db_path = '/home/lodek/bookpoint/bookpoint.db'

class Database(Session):

    """ Abstraction of the sqlite database containing the tables specified in model. 
    This class extends Sql Alchemy's Session class and add methods pertinent to the operations needed by bookpoint"""
    
    def __init__(self, db_fp=''):
        self.db_fp = db_fp if db_fp != '' else db_path
        self.base = declarative_base()
        self.engine = create_engine('sqlite:///'.format(self.db_fp), echo=True)
        super().__init__(bind=self.engine)
        self._create_db()
        #names to ease queries
        self.q_note = lambda _ : self.query(Noten)
        self.q_tag = lambda _ : self.query(Tag)
        self.q_mark = lambda _ : self.query(Mark)
        self.q_category = lambda _ : self.query(Category)
        
                   
    def _create_db(self):
        """ method that creates the database file and all tables as defined by the mapper classes in model.py"""
        logging.info('Creating Database')
        self.base.metadata.create_all(self.engine)
        
    def clean(self):
        """ removes any and all orphan entries in the database.
        orphan categories are categories with no marks
        orphan marks are marks with no categories
        orphan tags are tags with no marks
        orphan notes are notes with no marks """
        logging.info('Cleaning orphans in database')
        rm_categories = [category for category in self.get_all_category() if category.marks == []]
        self._remove_objs_in(rm_categories)
        logging.debug('Removed {} Category objects from DB'.format(len(rm_categories)))
        rm_marks = [mark for mark in self.get_all_mark() if not mark.category]
        self._remove_objs_in(rm_marks)
        logging.debug('Removed {} Mark objects from DB'.format(len(rm_marks)))
        rm_tags = [tag for tag in self.get_all_tag() if tag.marks == []]
        self._remove_objs_in(rm_tags)
        logging.debug('Removed {} Tag objects from DB'.format(len(rm_tags)))
        rm_notes = [note for note in self.get_all_note() if not note.mark]
        self._remove_objs_in(rm_notes)
        logging.debug('Removed {} Note objects from DB'.format(len(rm_note)))
        self.commit()
        removed_count = len(rm_marks) + len(rm_categories) + len(rm_tags) + len(rm_notes)
        logging.info('Removed {} objects on total'.format(removed_count))
        return

    def _remove_objs_in(self, list):
        """ removes all elements in list from database and commits it"""
        for element in list:
            self.delete(element)
        self.commit()
        logging.debug('Removed {} objects of type {} from database'.format(len(list),type(list[0])))
        return

        
    #returns all objects of a given type currently existing in the db
    def get_all_tag(self):
        return self._get_all(Tag)
        
    def get_all_mark(self):
        return self._get_all(Mark)
        
    def get_all_note(self):
        return self._get_all(Note)
        
    def get_all_category(self):
        return self._get_all(Category)
        
    def _get_all(self, table):
        return self.query(table).all()
