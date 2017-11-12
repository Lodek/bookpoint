from bookpoint.lib import lib
from bookpoint import session_db, app
from flask import Flask, render_template, request
from bookpoint.model.model import Category, Mark, Tag

def home():
    readinq_list = [q for q in session.query(Mark).order_by(Mark.date_added).filter(Mark.category_id == 1).all()]
    return render_template('readingq/home.html', readingq=readingq_list)

def new():
    return render_template('readingq/new.html')

def create():
    readingq_id= 1
    url=request.form['url']
    title = get_title(url)
    notes = request.form['notes']
    
    entry = Mark(url=url, title=title, notes=notes, category_id=readingq_id)
    session.add(entry)
    session.commit()
    return ##redirect user to readingq/home

