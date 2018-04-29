from db import Database
from model import Category, Mark, Tag
import utils
import unittest

utils.setup_logger()
db_fp = 'test-files/test.db'
org_fp = 'test-files/test.org'

class ModelBase(unittest.TestCase):
    def setUp(self):
        self.db = Database(db_fp)

class CategoryTester(ModelBase):
    def test_category_raw(self):
        category_raw = '* test_category'
        cat = Category.get_from_raw(category_raw, self.db)
        self.assertEqual(cat.name, 'test_category')

        
class TagTester(ModelBase):
    def test_single_tag(self):
        tags = Tag.get_from_raw(':test:', self.db)
        self.assertEqual(tags[0].name, 'test')

    def test_no_tag(self):
        tags = Tag.get_from_raw('::', self.db)
        self.assertEqual(tags, [])

    def test_multiple_tag(self):
        tags_string = ['potato' ,'bacon']
        tags = Tag.get_from_raw(':potato:bacon:', self.db)
        for expected, returned in zip(tags_string, tags):
            self.assertEqual(expected, returned.name)


class MarkTester(ModelBase):
    def test_min(self):
        raw = '** [[url]]'
        mark = Mark.get_from_raw(raw, self.db)
        self.assertEqual('url', mark.url)

    def test_title(self):
        raw = '** [[url][title]]'
        mark = Mark.get_from_raw(raw, self.db)
        self.assertEqual('url', mark.url)
        
    def test_min(self):
        raw = '** [[url]] (11/11/11)'
        mark = Mark.get_from_raw(raw, self.db)
        self.assertEqual('url', mark.url)
        
    def test_min(self):
        raw = '** [[url][title]] (11/11/11)'
        mark = Mark.get_from_raw(raw, self.db)
        self.assertEqual('url', mark.url)

        
class OrgTester(ModelBase):
    def setUp(self):
        self.org = Org(org_fp, self.db)
        
    def test_reader(self):
        self.org._read_org()
        self.assertNotIn('', self.org.body)

    def test_parser(self):
        self.org._parse_org()
        self.assertNotEqual([], self.org.marks)
        self.assertNotEqual([], self.org.tags)
        self.assertNotEqual([], self.org.categories)
