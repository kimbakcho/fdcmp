from test import BASE_DIR


def setLogger(loggerName: str,filePath: str):
    import logging
    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s')
    filehandler = logging.FileHandler(filePath)
    filehandler.setFormatter(formatter)
    consoleHandler = logging.StreamHandler()
    logger.addHandler(filehandler)
    logger.addHandler(consoleHandler)
