import sqlite3
from threading import Lock, Thread, Event

#TODO: autosave data thread

DATABASE_NAME = 'test.db'

def thread(fn):
    def run(*k, **kw):
        t = Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t
    return run

class SQLLiteOrm(object):
    def __init__(self, debug=False):
        self.conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.lock = Lock()
        self._event = Event()
        self._object_list = []
        self.debug = debug

    @thread
    def run(self):
        if self.debug:
            print('SQLLiteOrm thread started')

        while not self._event.wait(10):
            for obj in self._object_list:
                obj.save()

    def exit(self):
        self._event.set()

    def add_object(self, obj):
        self._object_list.append(obj)

    def save_table(self, obj):
        if self.debug:
            print('TABLE NAME: ', obj.__class__.__name__)
            print('TABLE: ', obj.__dict__)
            print('TABLE KEYS: ', obj.__dict__.keys())
        table_name = obj.__class__.__name__

        with self.lock:
            try:
                self.cursor.execute('DROP TABLE ' + table_name)
            except:
                pass

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS ''' + table_name + ''' ( variable text, value text )''')

            for key in obj.__dict__:
                self.cursor.execute("INSERT INTO " + table_name + " VALUES ('" + str(key) + "' , '" + str(obj.__dict__[key]) + "')")
                self.conn.commit()

    def read_table(self, obj):
        table_name = obj.__class__.__name__
        result_dict = {}
        keys = obj.__dict__.keys()

        with self.lock:
            for key in keys:
                try:
                    self.cursor.execute('SELECT * FROM ' + table_name + ' WHERE variable=?', (key,))
                except:
                    return result_dict
                result = self.cursor.fetchall()

                if len(result):
                    result_dict[key] = result[0][1]

        if self.debug:
            print('RESULT DICT: ', result_dict)
        return result_dict


class Table(object):
    def get_vars(self):
        return self.__dict__

    def save(self):
        sql_orm.save_table(self)

    def init(self):
        result = sql_orm.read_table(self)

        for key, value in result.items():
            self.__setattr__(key, value)

        sql_orm.add_object(self)

    def __del__(self):
        self.save()


class TableObject(object):
    def __init__(self):
        self._list = []

    def add_table(self, obj):
        if obj not in self._list:
            self._list.append(obj)

    def save_all(self):
        pass


sql_orm = SQLLiteOrm(debug=False)

sql_orm.run()

#USAGE EXAMPLE:
# class Car(Table):
#     def __init__(self):
#         self.some_var = '4'
#         self.init()