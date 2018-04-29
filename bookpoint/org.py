from db import Database
from model import Category, Tag, Mark
import utils
import logging, re

utils.setup_logger()
logger = logging.getLogger('bookpoint.org')

class Org():

    """ Represents a bookpoint org file, it takes a database SQLAlchemy session object and bookpoint org file as arguments.
    Org.update() parses the bookpoint file and generates the appropriate objects with all of their relationships and commits the database.
    Org.generate() reads the .db file and writes the .org file. """

    
    def __init__(self, org_fp, db):
        self.db = db
        self.org_fp = org_fp
        self.categories = []
        self.marks = []
        self.tags = []
        logger.info('Instance of Org created. self.org_fp = {}'.format(self.org_fp))

    def _read_org(self):
        """ Opens the org file defined on org_fp, reads it, removes new lines and assigns it to self """
        #should add error handler here, if file doesn't exist, exit
        with open(self.org_fp, 'r') as f:
            self.body = [line.strip() for line in f if line != '\n']
        logger.info('{} lines retrieved from org file'.format(len(self.body)))


    def _parse_org(self):
        """ Function responsible for identifying what each line in the org file represents and retrieving the 
        appropriate objects """
        regex_cat = r'^\* '
        regex_mark = '^\*\* '
        regex_note = r'^[^*]'
        db = self.db
        org = (line for line in self.body)
        current_category = Category.get_from_raw(next(org), db)
        logger.info('First Category {}'.format(current_category.name))
        current_mark = Mark.get_from_raw(next(org), db)
        logger.info('First Mark {}'.format(current_mark.url))
        current_mark.category = current_category
        current_category.marks.append(current_mark)
        self.marks.append(current_mark)
        self.categories.append(current_category)
        note_lines = []
        for line in org:
            logger.info('Current line "{}"'.format(line))
            if self._is_element(regex_note, line):
                note_lines.append(line)
            else:
                current_mark.notes = '\n'.join(note_lines)
                note_lines = []
                if self._is_element(regex_mark, line):
                    match = re.search(utils.regexes['splitter'], line)
                    mark = Mark.get_from_raw(match.group(1), db)
                    current_mark = mark
                    tags = Tag.get_from_raw(match.group(2), db)
                    current_mark.tags = tags
                    self.tags.extend(tags)
                    self.marks.append(mark)
                    current_category.marks.append(mark)
                elif self._is_element(regex_cat, line):
                    category = Category.get_from_raw(line, db)
                    current_category = category
                    self.categories.append(category)
        current_mark.notes = '\n'.join(note_lines)
        self.marks = list(set(self.marks))
        self.categories = list(set(self.categories))
        self.tags = list(set(self.tags))

        
    def update_db(self):
        """ Method responsible for reading the org file, parsing it and generating mapper objects. """
        logger.info('Begin parsing org file')
        self._read_org()
        self._parse_org()
        objs = self.marks + self.tags + self.categories
        self.db.add_and_commit(objs)
        self.write_org()
        #save copy of db
        #db.clean()
        #commit db
        logger.info('Done updating bookpoint!')
        return

    def write_org(self):
        """ Generates an org file for the database specified in self.db, the org file is written to self.org_fp """
        logger.info('Writing new org file')
        db = self.db
        categories = db.query(Category).all()
        with open(self.org_fp, 'w') as f:
            for category in categories:
                f.write('* {}\n'.format(category.name))
                for mark in category.marks:
                    tags = [tag.name for tag in mark.tags]
                    f.write('** [[{}][{}]] ({}) :{}:\n'.format(mark.url, mark.title, mark.date, ':'.join(tags)))
                    f.write(mark.notes+'\n')
        logger.info('Done writing file')
        return

    def _is_element(self, regex, line):
        return True if re.search(regex, line) else False


if __name__ == '__main__':
    db = Database('test-files/test.db')
    org = Org('test-files/test.org', db)
