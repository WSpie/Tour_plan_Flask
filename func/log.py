import logging
import os


logger = logging.getLogger(__name__)
handler = logging.FileHandler(os.path.abspath(os.path.join('log', 'sqlcheck.log')))
formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'
    )
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
