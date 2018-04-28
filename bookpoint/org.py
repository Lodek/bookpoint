from db import Database
from model import Category, Tag, Mark
import utils
import logging, re

logger = logging.getLogger(__name__)

class Org():

    """ Represents a bookpoint org file, it takes a database SQLAlchemy session object and bookpoint org file as arguments.
    Org.update() parses the bookpoint file and generates the appropriate objects with all of their relationships and commits the database.
    Org.generate() reads the .db file and writes the .org file. """
        
    def __init__(self, db, org_fp):
        # find better way to store/configure all these paths
        self.db = db
        self.org_fp = org_fp
        self.categories = []
        self.marks = []
        self.notes = []
        self.tags = []
        logger.info('Instance of Org created. self.org_fp = {} self.db.path_to_db = FIGURE IT OUT'.format(self.org_fp))

    def _read_org(self):
        """ Opens the org file defined on org_fp, reads it, removes new lines and assigns it to self """
        #should add error handler here, if file doesn't exist, exit
        with open(self.org_fp, 'r') as f:
            self.org = (line.strip() for line in f if line != '\n')
        logger.info('{} lines read from org file'.format(len(self.org_fp, self.org)))
        
    def update_db(self):
        """ Method responsible for reading the org file, parsing it and generating mapper objects. """
        logger.info('Begin parsing org file')
        _read_org()
        db = self.db
        current_category = Category.get_from_raw(next(self.org))
        current_mark = Mark.get_from_raw(next(self.org))
        current_category.marks.append(current_mark)
        self.marks.append(current_mark)
        self.categories.append(current_category)
        note_lines = []
        for line in self.org:
            if is_note(line):
                note_lines.append(line)
            else:
                current_mark.note = '\n'.join(note_lines)
                note_lines = []
                if is_mark(line):
                    match = re.search(utils.regexes['splitter'], line)
                    mark = Mark.get_from_raw(match(1))
                    current_mark = mark
                    tags = Tag.get_from_raw(match(2))
                    current_mark.tags = tags
                    self.tags.extend(tags)
                    self.marks.append(mark)
                    current_category.marks.append(mark)
                elif is_category(line):
                    category = Category.get_from_raw(line)
                    current_category = category
                    self.categories.append(category)
        current_mark.note = '\n'.join(note_lines)
        #save copy of db
        db.clean()
        #commit db
        self.update_org()
        logger.info('Done updating bookpoint!')
        return

    def update_org(self):
        """ Generates an org file for the database specified in self.db, the org file is written to self.org_fp """
        logger.info('Writing new org file')
        db = self.db
        categories = db.get_all_category()
        with open(self.org_fp, 'w') as f:
            for category in db:
                f.write('* {}\n'.format(category.name))
                for mark in category.marks:
                    tags = [tag.name for tag in mark.tags]
                    f.write('** [[{}][{}]] ({}) :{}:\n'.format(mark.url, mark.title, mark.date, ''.join(tags)))
                    f.write(mark.notes[0].body+'\n')
        logger.info('Done writing file')
        return
