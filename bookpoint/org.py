from db import Database
import re
import lib

org_path = 

class Org():

    """ Abstraction of the org file that contains the text version of the database. 
    It cotains methods for reading an org file and updating the database accordingly and also to generate a new org file given a database. 
    The hirearchy of the org file is categories at its highest level. categories contains marks and marks contains notes. """
        
    def __init__(self):
        self.db_session = Database().session
        self.categories = []
        self.org_fp = org_path
        self.org_body = []


    def _read_org(self):
        """ Opens the org file defined on org_fp, removes new lines and returns a list containing the lines """
        with open(self.org_fp, 'r') as f:
            self.org_body = [line.strip('\n') for line in f.readlines()]
        #log write info read file, x lines read
        
    def update_db(self):
        """ Method responsible for reading the text org file, parsing it and generating a database accordingly.
        The database is generating from "top down" which in this context means the highest hierarchy level down to the lower ones,
        that is, first all categories are parsed and generated. An iteration is made over each category and each mark is generated dynamically
        along with the notes"""
        #log info starting database update
        _read_org()
        self._parse_raw_categories()
        for category in self.categories_raw:
            self.categories.append(Category.get_from_raw(category))
        #log debug retrieved category objects %d category objects total
        for category in self.categories:
            marks_splitted = _parse_marks_raw(category.marks_raw)
            marks = [Mark.get_from_raw(mark) for mark in marks_splitted]
            #log debug fetched mark objects for category {category.name}, len(marks) objects retreived
            for mark in marks:
                tags_splitted = _parse_marks_raw(mark.tags_raw)
                mark.tags = [ Tag.get_from_raw(tag) for tag in tags_splitted]
                #log debug fetched tag objects for mark {mark.id}, len(marks.tags) objects retrieved
                if mark.notes == []:
                    mark.notes = [Note()]
                mark.notes[0].body =  mark.notes_raw
                #log debug set notes for mark {mark.id}
            #log debug category {category.name} received {len(marks)} marks.
            category.marks = marks
        #log info generated all marks, notes and tags objects, updating db session
        db_session.add_all(self.categories)
        db_session.commit()
        #log info done adding new objects
        self.clean_db()
        self.update_file()
        #log info done updating bookpoint!
        return

    def update_file(self):
        #log info writing new org file
        db = db_session.query(Category).all()
        with open(self.filepath, 'w') as f:
            for category in db:
                f.write('* {}\n'.format(category.name))
                for mark in category.marks:
                    tags = [tag.name for tag in mark.tags]
                    f.write('** {} - [[{}][{}]] ({}) :{}:\n'.format(mark.id, mark.url, mark.title, mark.date, ''.join(tags)))
                    f.write(mark.notes[0].body+'\n')
        return

    def clean_db(self):
        #log info cleaning orphans in database
        rm = lambda obj : db_session.delete(obj)
        
        rm_categories = [category for category in db_session.query(Category).all() if category.marks == []]
        #log debug found {len(rm_categories)} category objects to remove
        rm_marks = [mark for mark in db_session.query(Mark).all() if not mark.category]
        #log debug found {len(rm_marks)} mark objects to remove
        rm_tags = [tag for tag in db_session.query(Tag).all() if tag.marks == []]
        #log debug found {len(rm_tags)} tag objects to remove
        rm_notes = [note for note in db_session.query(Note).all() if not note.mark]
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
            self.db_session.delete(element)
        return
    
    def _parse_raw_categories(self):
        """ Takes the read org file to generate a list where each element matches a category block on the org file
        eg [['* Category 1', '** 1 ID - [[url-mark1][title-mark1]]',..],..].
        updates self with the split categories. """
        regex = lib.regexes['categories']
        self.categories_raw = self._parser(regex, self.body)
        #log info parsed categories %d categories found
        #log debug found categories = [category[0] for category in self.categories_raw]
        return
                

    def _parse_marks_raw(self, marks_raw):
        """ Takes the mark_raw list and returns a list of lists where each list is a mark as defined in the org fomat.
        sample output [['** ID - URL :tags:','notes'],['** ID - Other_URL :tags:','notes']]"""
        regex = lib.regexes['marks']
        marks_splitted = _parser(regex,marks_raw)
        #log debug parsed raw marks, found len(marks_splitted) marks
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
