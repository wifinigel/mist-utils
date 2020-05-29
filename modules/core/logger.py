"""
A simple logging function to log operations and messages when running a script
"""

import logging

def ScriptLogger(name, log_level=logging.INFO):

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # set up logging to console

    ## create console handler & set level
    console_handler = logging.StreamHandler()

    ## create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ## add formatter to console handler
    console_handler.setFormatter(formatter)

    ## add console handler to logger
    logger.addHandler(console_handler)

    return logger
