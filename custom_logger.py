import logging, logging.handlers

class MyLogger:
    def init():
        _logger = logging.getLogger('custom_logger')
        _logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler('logger.log')
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(levelname)-8s][%(threadName)-10s][%(asctime)s] - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        _logger.addHandler(fh)
        _logger.addHandler(ch)

        return _logger


logger = MyLogger.init()

logger.info('Logger init')
