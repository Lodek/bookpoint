from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from model import Category, Mark, Tag, Base
import logging

logger = logging.getLogger(__name__)

class Database(Session):

    """ Abstraction of the sqlite database containing the tables specified in model. 
    This class extends Sql Alchemy's Session class and add methods pertinent to the operations needed by bookpoint"""
    
    def __init__(self, db_fp):
        self.db_fp = db_fp
        self.base = Base
        self.engine = create_engine('sqlite:///'.format(self.db_fp), echo=False)
        super().__init__(bind=self.engine)
        self._create_db()
        #names to ease queries
                   
    def _create_db(self):
        """ method that creates the database file and all tables as defined by the mapper classes in model.py"""
        logger.info('Creating Database')
        self.base.metadata.create_all(self.engine)

    def _remove_objs_in(self, list):
        """ removes all elements in list from database and commits it"""
        for element in list:
            self.delete(element)
        self.commit()
        logger.debug('Removed {} objects of type {} from database'.format(len(list),type(list[0])))
        return
