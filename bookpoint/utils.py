import configparser, logging

regexes = {'marks':r'^\*\* \[\[(.*?)\](?:\[.*\])?\](?: \(.*\))? *(:.*:)?$',
           'categories' : r'^\* (.*)$',
           'notes' : r'^\*\*\* ([\d?]+)',
           }

def read_ini ():
    ini_fp = 'config.ini'
    config = configparser.ConfigParser()
    config.read(ini_fp)
    return config

def setup_logger():
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('{asctime}|{levelname}|{name}|{funcName} - {message}',style='{')
    info_handler = logging.FileHandler('bookpoint_info.log')
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)
    debug_handler = logging.FileHandler('bookpoint_debug.log')
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)
    logger.addHandler(debug_handler)
    logger.addHandler(info_handler)
