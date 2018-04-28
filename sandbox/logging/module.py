import logging
import sys

def funk():
    logger = logging.getLogger(__name__)
    logger.info('funk')
    logging.info('root funk')
