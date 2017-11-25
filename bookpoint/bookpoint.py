import requests
import re
from flask import Flask
from sqlalchemy.orm import sessionmaker 
from bookpoint.model.model import Category, Mark, Tag, Base, engine 
from flask import Flask, render_template, request

app = Flask(__name__) 
Session = sessionmaker(bind=engine)
session = Session()

#Bookpoint Routes
@app.route('/')
def bookpoint_home():
    return render_template('bookpoint/home.html', marksd=get_full_db())

@app.route('/org')
def bookpoint_org():
    return render_template('bookpoint/org.html', marksd=get_full_db(), mark_tags=mark_tags)

@app.route('/new')
def bookpoint_new():
    return render_template('bookpoint/new.html')

@app.route('/create', methods=['POST'])
def bookpoint_create():
    category = request.form['category']
    url=request.form['url']
    title = get_title(url)
    notes = request.form['notes']
    tags = request.form['tags']
    new_mark = Mark(url=url, title=title, notes=notes)

    category_obj = session.query(Category).filter(Category.name == category).first()
    if category_obj is None:
        category_obj = Category(name=category)
    new_mark.category = category_obj

    tags = tags.split(' ')
    new_tags = []
    for tag in tags:
        ttag = session.query(Tag).filter(Tag.name == tag).first()
        if ttag is None:
            ttag = Tag(name=tag)
        new_tags.append(ttag)
    new_mark.tags = new_tags
    session.add(new_mark)
    session.commit()
    return render_template('bookpoint/home.html', marksd=get_full_db())


#Sessions routes
@app.route('/sessions/')
def sessions_home():
    return render_template('sessions/home.html', sessions=get_sessions_db())

@app.route('/sessions/orghome')
def sessions_orghome():
    return render_template('sessions/org.html', sessions=get_sessions_db())

@app.route('/sessions/new')
def sessions_new():
    return render_template('sessions/new.html')

@app.route('/sessions/create', methods=['POST'])
def sessions_create():
    urls = request.form['urls']
    notes = request.form['notes']
    category = request.form['category']

    sessiont = session.query(Tag).filter(Tag.name == 'session').first()
    category_obj = Category(name=category)
    urls =urls.split('\n')
    for url in urls:
        mark = Mark(url=url, title=get_title(url), notes=notes)
        mark.category = category_obj
        mark.tags = [sessiont]
        session.add(mark)
    session.commit()
    return render_template('sessions/home.html', sessions=get_sessions_db())


#Reading Queue routes
@app.route('/readingq/')
def readingq_home():
    return render_template('readingq/home.html', marks=get_readingq_db())

@app.route('/readingq/orghome')
def readingq_orghome():
    return render_template('readingq/org.html', marks=get_readingq_db())

@app.route('/readingq/new')
def readingq_new():
    return render_template('readingq/new.html')

@app.route('/readingq/create', methods=['POST'])
def readingq_create():
    url = request.form['url']
    title = get_title(url)
    notes = ''
    rq_obj = session.query(Category).filter(Category.name == 'readingq').first()
    mark = Mark(url=url, title=title, notes=notes)
    mark.category = rq_obj
    session.add(mark)
    session.commit()
    return render_template('readingq/home.html', marks=get_readingq_db())    


def get_readingq_db():
    rq_obj = session.query(Category).filter(Category.name == 'readingq').first()
    return rq_obj.mark

def get_full_db():
    categories = session.query(Category).all()
    db = {}
    for category in categories:
        db[category.name] = category.mark
    return db

def get_sessions_db():
    sessiont = session.query(Tag).filter(Tag.name == 'session').first()
    marks = sessiont.marks
    session_dic = {}
    for mark in marks:
        session_dic[mark.category.name] = []
    for mark in marks:
        session_dic[mark.category.name].append(mark)
    return session_dic

def get_title(url):
    # Discard exception for when the url is not valid or whatever
    try:
        obj=requests.get(url)
        title=re.findall('<title>(.*?)<\/title>',obj.text)
        title = title[0]
    except BaseException:
        title=url
    return title

def get_category_obj(category_name):
    category_obj = session.query(Category).filter(Category.name == category_name).first()

def mark_tags(mark):
    tags = [tag.name for tag in mark.tags]
    tags_str = ':'
    for tag in tags:
        tags_str += '{}:'.format(tag)
    return tags_str
