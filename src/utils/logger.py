import logging
import os

def setup_logger(name):
    logger = logging.getLogger(name)
    level = os.environ.get('LOG_LEVEL', 'INFO')
    logger.setLevel(level)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger 