import logging
import logging.handlers

class MyLogger:
    def init():
        _logger = logging.getLogger('custom_logger')
        _logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler('logger.log')
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        format_string = '[%(levelname)-8s][%(threadName)-10s][%(asctime)s] - %(message)s'

        formatter = logging.Formatter(format_string)
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
        for function_name in dct:
            if hasattr(dct[function_name], '__call__'):
                dct[function_name] = logfunc(dct[function_name], name)
        return type.__new__(cls, name, bases, dct)


logger = MyLogger.init()

logger.info('Logger init')
