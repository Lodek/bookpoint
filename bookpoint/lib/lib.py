def get_title(url):
    # Discard exception for when the url is not valid or whatever
    try:
        obj=requests.get(url)
        src_code=obj.text
        title=re.findall('<title>.*?</title>',src_code)
        title=title[0]
        title=title[:-8]
        title=title.strip('<title>')

    except BaseException:
        title=url
        
    return title
