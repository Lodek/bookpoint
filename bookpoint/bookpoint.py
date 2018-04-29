from db import Database
from model import Category, Mark, Tag
from org import Org
import utils
import argparse, logging, sys

logger = logging.getLogger('bookpoint.bookpoint')

def main():
    config = utils.read_ini()
    args = args_handler().parse_args()
    org_fp = args.org if args.org else config['paths']['org_fp']
    db_fp = args.db if args.db else config['paths']['db_fp']
    backup_path = config['paths']['backup_path']
    db = Database(db_fp)
    if args.command[0] == 'update':
        Org(db=db, org_fp=org_fp).update_db()
    elif args.command[0] == 'add':
        pass
        #Mark.add_mark()


def args_handler():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='*', default=['update'], help='command to be executed (update/add). default behavior is update')
    parser.add_argument('-d', '--db', help='optinal flag to specify the database file')
    parser.add_argument('-o', '--org', help='optional flag to specify the orgmode file')
    return parser


def backup(backup_dir, db_fp, org_fp):
    backup_dir = os.path.expanduser(backup_dir)
    try:
        os.mkdir(backup_dir)
    except:
        sys.exit('Backup directory could not be created')

    
if __name__ == "__main__":
    main()
