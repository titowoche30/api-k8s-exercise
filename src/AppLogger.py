import logging


def get_logger():
    logging.basicConfig(format='%(levelname)s:      %(asctime)s %(message)s',
                        datefmt='%I:%M:%S %p %Z',
                        level=logging.INFO)
    logger = logging.getLogger()

    return logger
