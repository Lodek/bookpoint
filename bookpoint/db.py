from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class Database(Session):
    def __init__(self):
        self.engine = create_engine('sqlite:///'.format(self.db_path), echo=True)
        super().__init__(bind=self.engine)
        #number of each object initially        
        self.tags_n = self.query.(Tag).count()
        self.marks_n = self.query.(Mark).count()
        self.notes_n = self.query.(Note).count()
        self.categories_n = self.query.(Category).count()
        
        self.db_path = db_path
        self.org_path = org.path
        self.base = declarative_base()

        
class Database():

    """ Class that interfaces with sql alchemy generating the session object that is utilized to add/remove things to database """
    
    db_path = '/home/lodek/bookpoint/bookpoint.db'
    org_path = '/home/lodek/bookpoint/bookpoint.org'
    
    def __init__(self, db_path=Database.db_path, org_path=Database.org_path):
        self.db_path = db_path
        self.org_path = org.path
        self.base = declarative_base()

        
        
    def create_db(self):
        #log info creating database
        self.base.metadata.create_all(self.engine)
        
    def clean_db(self):
        #log info cleaning orphans in database
                
        rm_categories = [category for category in self.query(Category).all() if category.marks == []]
        #log debug found {len(rm_categories)} category objects to remove
        rm_marks = [mark for mark in self.query(Mark).all() if not mark.category]
        #log debug found {len(rm_marks)} mark objects to remove
        rm_tags = [tag for tag in self.query(Tag).all() if tag.marks == []]
        #log debug found {len(rm_tags)} tag objects to remove
        rm_notes = [note for note in self.query(Note).all() if not note.mark]
        #log debug found {len(rm_notes)} note objects to remove

        self._remove_objs_in(rm_categories)
        self._remove_objs_in(rm_marks)
        self._remove_objs_in(rm_tags)
        self._remove_objs_in(rm_notes)

        removed_count = len(rm_marks) + len(rm_categories) + len(rm_tags) + len(rm_notes)
        #log info removed {removed_count} objects from databse
        return

    def _remove_objs_in(self, list):
        """ removes all elements in list from database """
        for element in list:
            self.rm(element)
        return
