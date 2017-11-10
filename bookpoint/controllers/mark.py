from bookpoint import session, app
from flask import Flask, render_template, request
from bookpoint.model.model import Category, Mark, Tag, Base, engine

def home():
    mark_dict = {}
    return render_template('mark/home.html', mark_dict=mark_dict)

def new():
    return render_template('mark/new.html')

def create():
    category = request.form['category']
    url=request.form['url']
    title = get_title(url)
    notes = request.form['notes']
    tags = request.form['tags']

    new_mark = Mark(url=url, title=title, notes=notes)

    
    session.add(entry)
    session.commit()
    return 'abort!'##redirect user to readingq/home

def get_marks_dict():
    for category in session.query(Category.name).all():
        marks_list = []
        for mark in session.query(Mark).filter(Mark.category.name == category).all():
            tags = ':'
            for tag in mark.tags:
                tags += '{}:'.format(tag.name)
            marks_list.append([mark,tags])
        mark_dict[category] = marks_list
