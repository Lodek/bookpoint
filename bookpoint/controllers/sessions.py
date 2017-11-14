from bookpoint.lib import lib
from bookpoint import session_db, app
from flask import Flask, render_template, request
from bookpoint.model.model import Category, Mark, Tag


def home():
    sessions_dict = get_sessions()
    return render_template('sessions/home.html', sessions_dict=sessions_dict)

def org():
    sessions_dict = get_sessions()
    return render_template('sessions/orghome.html', sessions_dict=sessions_dict)

def new():
    return render_template('sessions/new.html')

def create():
    tag_obj = session_db.query(Tag).filter(Tag.name == 'session').first()
    category = request.form['category']
    notes = request.form['notes']
    urls = request.form['urls']
    urls = urls.split('\n')
    for url in urls:
        title = lib.get_title(url)
        new_mark = Mark(url=url, title=title, notes=notes


def get_sessions():
    tag_obj = session_db.query(Tag).filter(Tag.name == 'sessions').first() #get tag obj for sessions
    mark_list = tag_obj.marks

    session_dict = {} #empty dict
    for mark in mark_list: #generates dictionary with empty lits
        session_dict[mark.category.name] = []
    for mark in mark_list:
        session_dict[mark.category.name].append(mark)
    return session_dict

