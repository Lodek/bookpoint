from bookpoint import session_db
import requests
import re

def get_title(url):
    # Discard exception for when the url is not valid or whatever
    try:
        obj=requests.get(url)
        title=re.findall('<title>(.*?)<\/title>',obj.text)
    except BaseException:
        title=url
    return title

def get_category_obj(category_name):
    category_obj = session_db.query(Category).filter(Category.name == category_name).first()
