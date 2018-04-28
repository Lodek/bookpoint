from db import Database
from model import Category, Note, Mark, Tag
from org import Org
import argparse
import logging

logger = logging.getLogger(__name__)

def main():
    args = args_handler().parse_args()
    org_fp = args.org if args.org else ''
    db_fp = args.db if args.db else ''

    db = Database(db_fp)
    if args.command[0] == 'update':
        Org(db,org_fp=org_fp).update_db()
    elif args.command[0] == 'add':
        #Mark.add_mark()


def args_handler():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='*', default=['update'], help='command to be executed (update/add). default behavior is update')
    parser.add_argument('-d', '--db', help='optinal flag to specify the database file')
    parser.add_argument('-o', '--org', help='optional flag to specify the orgmode file')
    return parser

if __name__ == "__main__":
    main()
