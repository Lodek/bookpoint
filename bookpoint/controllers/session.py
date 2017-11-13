from bookpoint.lib import lib
from bookpoint import session_db, app
from flask import Flask, render_template, request
from bookpoint.model.model import Category, Mark, Tag


def home():
    sessions = get_sessions
    return render_template('readingq/home.html', sessions=sessions)

def new():
    return render_template('readingq/new.html')

def create():
    tag_ses = session_db.query(Tag).filter(Tag.name == 'session')
    category = request.form['category']
    notes = request.form['notes']
    urls = request.form['urls']
    url_list = parse_urls(urls)


def get_sessions():
    tag_ses = session_db.query(Tag).filter(Tag.name == 'session') #query session tag obj
    mark_list = tag_ses.marks
    sessions = {}
    for mark in mark_list: #generates dictionary with empty list for every category
        sessions[mark.category]= []
    for mark in mark_list: #
        sessions[mark.category].append(mark)
    return sessions

def parse_urls(urls):
    return
