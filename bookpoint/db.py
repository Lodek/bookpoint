from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from model import Category, Mark, Tag, Base
import logging

logger = logging.getLogger('bookpoint.db')

class Database(Session):

    """ Abstraction of the sqlite database containing the tables specified in model. 
    This class extends Sql Alchemy's Session class and add methods pertinent to the operations needed by bookpoint"""
    
    def __init__(self, db_fp):
        self.db_fp = db_fp
        self.base = Base
        engine_path = 'sqlite:///{}'.format(self.db_fp)
        self.engine = create_engine(engine_path, echo=False)
        super().__init__(bind=self.engine)
        self._create_db()
        #names to ease queries
                   
    def _create_db(self):
        """ method that creates the database file and all tables as defined by the mapper classes in model.py"""
        logger.info('Creating Database')
        self.base.metadata.create_all(self.engine)

    def add_and_commit(self, objs):
        self.add_all(objs)
        self.commit()

if __name__ == '__main__':
    db = Database('test-files/test.db')
