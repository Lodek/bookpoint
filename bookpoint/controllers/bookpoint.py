from bookpoint.lib import lib
from bookpoint import session_db, app
from flask import Flask, render_template, request
from bookpoint.model.model import Category, Mark, Tag, Base, engine

def home():
    return render_template('bookpoint/home.html', mark_db=get_full_db())

def orghome():
    return render_template('bookpoint/orghome.html', mark_db=get_full_db())

def new():
    return render_template('bookpoint/new.html')

def create():
    category = request.form['category']
    url=request.form['url']
    title = lib.get_title(url)
    notes = request.form['notes']
    tags = request.form['tags']
    
    new_mark = Mark(url=url, title=title, notes=notes)
    #test request form dict for tags (new line and etc)
    session.add(entry)
    session.commit()
    return 'abort!'##redirect user to readingq/home

def get_full_db():
    db_dict = {}
    for category in session.query(Category.name).all():
        marks_list = []
        for mark in session.query(Mark).order_by(Mark.title).filter(Mark.category.name == category).all():
            tags = ':'
            for tag in mark.tags:
                tags += '{}:'.format(tag.name)
            mark.tags_str=tags
            marks_list.append(mark)
        mark_dict[category] = marks_list
    return db_dict
