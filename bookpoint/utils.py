import configparser, logging, os

regexes = {'marks':r'\*\* \[\[(.*?)\].*\]',
           'splitter':r'(\*\* \[\[.*\].*\] ?(?:[0-9-)( ]*)?)( *(?::.*:)?)',
           'categories' : r'^\* (.*)$'}

def read_ini ():
    ini_fp = 'config.ini'
    config = configparser.ConfigParser()
    config.read(ini_fp)
    return config

def setup_logger():
    join_path = lambda path, filename : os.path.join(os.path.expanduser(path), filename)
    path = read_ini()['paths']['logging_path']
    info_fp = join_path(path, 'bookpoint_info.log')
    debug_fp = join_path(path, 'bookpoint_debug.log')
    debug_all_fp = join_path(path, 'bookpoint_debug_all.log')
    logger = logging.getLogger('bookpoint')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('{asctime}|{levelname}|{name}|{funcName} - {message}',style='{')
    info_handler = logging.FileHandler(info_fp)
    debug_handler = logging.FileHandler(debug_fp)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)
    logger.addHandler(debug_handler)
    logger.addHandler(info_handler)
    logger_root = logging.getLogger('')
    logger_root.setLevel(logging.DEBUG)
    debug_root_handler = logging.FileHandler(debug_all_fp)
    debug_root_handler.setLevel(logging.DEBUG)
    debug_root_handler.setFormatter(formatter)
    logger_root.addHandler(debug_root_handler)
