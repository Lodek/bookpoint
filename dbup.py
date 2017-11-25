import re

class Mark():
    def __init__(self, title, url, tags):
        self.title=title
        self.url=url
        self.tags=tags

f = open('orgfile.txt', 'r')
orgin = f.read()
f.close()

categories = re.findall('^\* .*$', orgin, re.MULTILINE)
marks_by_cat = re.split('^\* .*$', orgin, flags=re.MULTILINE)
marks_by_cat = marks_by_cat[1:]

for marks in marks_by_cat:
    marks_parsed = re.findall('\*\* [0-9xX?]+ - \[\[.*\]\[.*\]\] :.*:(?:.*|[\s]*)*?(?=\*\*|\s$)', marks, flags=re.MULTILINE)
    for mark in marks_parsed:
        mark_ps= re.findall('\*\* ([0-9xX?]+) - \[\[(.*)\]\[(.*)\]\] :(.*):', mark)
        print(mark_ps)
