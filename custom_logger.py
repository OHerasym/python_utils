import logging, logging.handlers
import functools

class MyLogger(object):
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

def logfunc(func, class_name=None):
    def run(*args, **kwards):
        func_name = func.__name__
        if class_name:
            func_name = class_name + '.' + func.__name__
        logger.debug('start ' + func_name)
        func(*args, *kwards)
        logger.debug('finish ' + func_name)
    return run


class MetaLog(type):
    def __new__(cls, name, bases, dct):
        for m in dct:
            if hasattr(dct[m], '__call__'):
                dct[m] = logfunc(dct[m], name)
        return type.__new__(cls, name, bases, dct)


logger = MyLogger.init()

logger.info('Logger init')
