import module
import logging
import sys
#logging.basicConfig(format='{asctime}|{levelname}|{name}|{funcName} - {message}', level=logging.DEBUG, style='{')
#logging.info('hello')
logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('{asctime}|{levelname}|{name}|{funcName} - {message}',style='{')
info_handler = logging.StreamHandler(stream=sys.stdout)
info_handler.setFormatter(formatter)
logger.addHandler(info_handler)

logger.info('test')
logging.info('another test')
logging.getLogger(__name__).info('named test')
module.funk()
