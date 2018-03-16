import requests
import re


def get_title(url):
    # Discard exception for when the url is not valid or whatever
    try:
        obj=requests.get(url)
        title=re.search('<title>(.*?)<\/title>',obj.text).group(1).replace('[', '|').replace(']','|')
    except BaseException:
        title=url
    return title

regexes = {'marks':r'^\*\* \[\[(.*)\](?:\[.*\])?\] ?(?:\(.*\))? *(:.*:)?$',
           'categories' : r'^\* (.*)$',
           'notes' : r'^\*\*\* ([\d?]+)',
           }
