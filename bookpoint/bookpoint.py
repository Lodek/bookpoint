from db import Database
from model import Category, Note, Mark, Tag
from org import Org
import argparse

def main():
    parser = args_handler()
    args = parser.parse_args()
    if args.command[0] == 'update':
        Org().update_db()
    elif args.command[0] == 'add':
        Mark.add_mark() ###furthr optional argument should go there
    database.create_db()

def org():
    org = Org()
    org.update_db()

def new_mark(url):
    Mark.add_mark(url=url)
    
def args_handler():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='*', default=['update'], help='command to be executed (update/add). default behavior is update')
    parser.add_argument('-i', '--in', help='optinal flag to specify the database file to be read')
    parser.add_argument('-o', '--out', help='optional flag to specify the output orgmode file')
    return parser
