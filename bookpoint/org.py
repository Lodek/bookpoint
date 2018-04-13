from db import Database
import logging
import re
import lib

org_path = '/home/lodek/bookpoint/bookpoint.org'

class Org():

    """ Abstraction of the org file that contains the text version of the database. 
    It cotains methods for reading an org file and updating the database accordingly and also to generate a new org file given a database. 
    The hirearchy of the org file is categories at its highest level. categories contains marks and marks contains notes. """
        
    def __init__(self, db, org_fp=''):
        self.db = db
        self.org_fp = org_path if org_path != '' else org_path

    def _read_org(self):
        """ Opens the org file defined on org_fp, reads it, removes new lines and assigns it to self """
        #should add error handler here, if file doesn't exist, exit
        with open(self.org_fp, 'r') as f:
            self.org_body = [line.strip('\n') for line in f.readlines()]
        logging.info('read {}. {} lines read'.format(len(self.org_fp, self.org_body)))
        
    def update_db(self):
        """ Method responsible for reading the text org file, parsing it and generating a database accordingly.
        The database is generating from "top down" which in this context means the highest hierarchy level down to the lower ones,
        that is, first all categories are parsed and generated. An iteration is made over each category and each mark is generated dynamically
        along with the notes"""
        logging.info('starting database update')
        _read_org()
        db = self.db
        self._parse_raw_categories()
        self.categories = [Category.get_from_raw(category, db=db) for category in self.categories_raw]
        logging.debug('Retrieved {} Category objects.'.format(len(self.categories)))
        for category in self.categories:
            marks_splitted = _parse_marks_raw(category.marks_raw)
            marks = [Mark.get_from_raw(mark, db=db) for mark in marks_splitted]
            logging.debug('Fetched Mark objects for category {}. {} objects retreived'.format(category.name, len(marks)))
            for mark in marks:
                tags_splitted = _parse_marks_raw(mark.tags_raw)
                mark.tags = [ Tag.get_from_raw(tag, db=db) for tag in tags_splitted]
                logging.debug('Fetched Tag objects for mark {}. {}  objects retrieved'.format(mark.id, len(marks.tags)))
                if mark.notes == []:
                    mark.notes = [Note()]
                mark.notes[0].body =  mark.notes_raw
                logging.debug('Set notes for mark {}'.format(mark.id))
            category.marks = marks
            logging.debug('Category {} received {} marks.'format(category.name, len(marks)))
        logging.info('Generated all marks, notes and tags objects, updating db session')
        db.add_all(self.categories)
        db.commit()
        logging.info('Done adding new objects')
        db.clean()
        self.update_org()
        logging.info('Done updating bookpoint!')
        return

    def update_org(self):
        """ Generates an org file for the database specified in self.db, the org file is written to self.org_fp """
        logging.info('Writing new org file')
        db = self.db
        categories = db.get_all_category()
        with open(self.org_fp, 'w') as f:
            for category in db:
                f.write('* {}\n'.format(category.name))
                for mark in category.marks:
                    tags = [tag.name for tag in mark.tags]
                    f.write('** [[{}][{}]] ({}) :{}:\n'.format(mark.url, mark.title, mark.date, ''.join(tags)))
                    f.write(mark.notes[0].body+'\n')
        logging.info('Done writing file')
        return

     def _parse_raw_categories(self):
        """ Takes the read org file to generate a list where each element matches a category block on the org file
        eg [['* Category 1', '** 1 ID - [[url-mark1][title-mark1]]',..],..].
        updates self with the split categories. """
        regex = lib.regexes['categories']
        self.categories_raw = self._parser(regex, self.body)
        logging.info('Parsed Categories. {} categories found'.format(len(self.categories_raw)))
        logging.debug('self.categories_raw = {}'.format(self.categories_raw))
        return
                

    def _parse_marks_raw(self, marks_raw):
        """ Takes the mark_raw list and returns a list of lists where each list is a mark as defined in the org fomat.
        sample output [['** ID - URL :tags:','notes'],['** ID - Other_URL :tags:','notes']]"""
        regex = lib.regexes['marks']
        marks_splitted = _parser(regex,marks_raw)
        logging.debug('parsed raw marks, found {} marks'.format(len(marks_splitted)))
        return mark_splitted

    def _parse_tags_raw(self, tags_raw):
        """ Method parses the tag_raw string. 
        sample input ":tag1:tag2:...:tagn:"
        sample out ['tag1','tag2',...]"""
        tags_splitted = tags_raw[1:-1].split(':')
        return tags_splitted

    
    def _parser(self, regex, list):
        """ Main parser method. This method is used as the core logic for parsing categories, marks and notes (since the logic is very similar)
        The method matches a regex on each element of a list. Essentially it splits a list using the regex
        and uses matches as places to start and end the sub lists.
        This method isn't called on itself, instead it is used to build the other parser functions"""
        matches = [index for index, line in enumerate(list) if re.search(regex, line)]
        matches.append(len(list))
        parsed_list = [list[matches[index]:matches[index+1]] for index in range(len(matches)-1)]
        return parsed_list
