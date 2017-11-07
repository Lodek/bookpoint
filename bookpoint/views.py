import requests
import re
from bookpoint import app

@app.route('/')
def home():
  return render_template('home.html', url_list=get_list())

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/add/bookmark', methods=['POST'])
def add_bookmark():
    url=request.form['url']
    title=get_title(url)
    mark='<a href="{}"> {} </a><br>'.format(url,title)

    with open('templates/list.html', 'a') as list_file:
        list_file.write(mark)
    list_file.close()
    return render_template('home.html', url_list=get_list())

if __name__ == '__main__':
  app.run(debug=True)

def get_title(url):
    # Discard exception for when the url is not valid or whatever
    try:
        obj=requests.get(url)
        src_code=obj.text
        title=re.findall('<title>.*?<',src_code)
        title=title[0]
        title=title[:-1]
        title=title.strip('<title>')

    except BaseException:
        title=url
        
    return title

def get_list():
    with open('templates/list.html', 'r') as list_file:
        urls=list_file.readlines()
    list_file.close()

    urls = [url.strip('\n') for url in urls]

    list_page=''
    for url in urls:
        list_page = list_page + url
    return list_page

def remove_entry(id):
    with open('templates/list.html', 'r') as list_file:
        urls=list_file.readlines()
    list_file.close()

    new_url_list=[]
    for counter, url in enumerate(urls):
        if not (counter == id):
            new_url_list.append(url)

    with open('templates/list.html', 'w') as list_file:
        for url in new_url_list:
            list_file.write(url)
    list_file.close()
