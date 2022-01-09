from custom_logger import logger

def thread(fn):
    def run(*k, **kw):
        t = Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t
    return run

def check_error(func):
    def run(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(func.__name__ + ' error: ', e)
    return run

class ErrorHandler(type):
    def __new__(cls, name, bases, dct):
        for m in dct:
            if hasattr(dct[m], '__call__'):
                dct[m] = check_error(dct[m])
        return type.__new__(cls, name, bases, dct)

class MetaLock(type):
    def __new__(cls, name, bases, dct):
        lock = Lock()

        for m in dct:
            if hasattr(dct[m], '__call__'):
                dct[m] = lockfunc(dct[m], lock)
        return type.__new__(cls, name, bases, dct)


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def remove_file(file_name):
        try:
            os.remove(file_name)
        except Exception as e:
            print(e)

    @staticmethod
    def current_time_str():
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def dt_from_str_time(str_time):
        if str_time:
            return datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')
        return None


    @staticmethod
    def translate(string):
        translation_table = str.maketrans("абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ", 
                                          "abvgdeezziiklmnoprstyphchhh____yaabvgdeezziiklmnoprstyphchhh____ya")

        return string.translate(translation_table)

    @staticmethod
    def set_to_string(sset):
        result = ''
        if len(sset) != 0:
            for s in sset:
                result += s + ', '
        else:
            result = 'Empty Set'
        return result