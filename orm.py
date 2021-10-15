import sqlite3
from threading import Lock, Thread, Event
import inspect

from error_manager import em

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

    def all_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return self.cursor.fetchall()

    def check_table(self, table_name):
        tables = self.all_tables()

        for table in tables:
            if table[0] == table_name:
                return True
        return False

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

    def drop(self, table_name):
        with self.lock:
            try:
                if self.debug:
                    print('DROP TABLE ' + '"'+ table_name + '"')
                self.cursor.execute('DROP TABLE ' + '"'+ table_name + '"')
            except Exception as e:
                if self.debug:
                    print('ERROR: drop table fail: ', e)

    def save_table(self, obj):
        if self.debug:
            print('TABLE NAME: ', obj.__class__.__name__)
            print('TABLE: ', obj.__dict__)
            print('TABLE KEYS: ', obj.__dict__.keys())
        table_name = obj.__class__.__name__

        with self.lock:
            try:
                if self.debug:
                    print('DROP TABLE ' + '"'+ table_name + '"')
                self.cursor.execute('DROP TABLE ' + '"'+ table_name + '"')
            except:
                if self.debug:
                    print('ERROR: drop table fail')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS ''' + '"'+ table_name + '"' + ''' ( variable text, value text )''')

            for key in obj.__dict__:
                self.cursor.execute("INSERT INTO " + '"'+ table_name + '"' + " VALUES ('" + str(key) + "' , '" + str(obj.__dict__[key]) + "')")
                self.conn.commit()


    def read_table(self, obj):
        table_name = obj.__class__.__name__
        result_dict = {}
        keys = obj.__dict__.keys()

        with self.lock:
            for key in keys:
                try:
                    self.cursor.execute('SELECT * FROM ' + '"'+ table_name + '"' + ' WHERE variable=?', (key,))
                except:
                    return result_dict
                result = self.cursor.fetchall()

                if len(result):
                    result_dict[key] = result[0][1]

        if self.debug:
            print('RESULT DICT: ', result_dict)
        # print('RESULT DICT: ', result_dict)
        return result_dict

    def read_table_list(self, obj):
        table_name = obj.__class__.__name__

        if self.debug:
            print('TABLE NAME: ', obj.__class__.__name__)
            print('TABLE KEYS: ', obj.__dict__.keys())

        with self.lock:
            query = '( '

            for key in obj.__dict__.keys():
                if key != '_list':
                    query += key + ' text, '

            query = query[:-2] + ' )'

            if self.debug:
                print('QUERY: ', query)

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS ''' + table_name + query)

            self.cursor.execute("SELECT * FROM " + table_name)
            result = self.cursor.fetchall()
            print('RESULT LEN: ',len(result))

            return result


    def add_table_obj(self, this, obj):
        table_name = this.__class__.__name__

        try:
            with self.lock:
                query = "('" 

                for value in obj.__dict__.values():
                    value = value.replace("'",':::')
                    query += value + "', '"

                query = query[:-4] + "')"
                if self.debug:
                    print('QUERY: ', query)

                self.cursor.execute("INSERT INTO " + table_name + " VALUES " + query)
                self.conn.commit()
        except Exception as e:
            print('ERROR: ', e)
            em.new_error()

    def edit_table_obj(self, this, obj):
        table_name = this.__class__.__name__
        if self.debug:
            print('EDIT TABLE NAME: ', table_name)

        try:
            with self.lock:
                query = ""

                for var, value in obj.__dict__.items():
                    if self.debug:
                        print(var, value)
                    query += str(var) + " = '" + str(value) + "',"

                w_id, w_value = next(iter(obj.__dict__.items()))
                w = " WHERE " + str(w_id) + " = " + "'" + str(w_value) + "'"
                query = query[:-1]

                # print('QUERY: ', query[:-1], w)

                q = "UPDATE " + table_name + " SET " + query + w
                if self.debug:
                    print(q)
                self.cursor.execute("UPDATE " + table_name + " SET " + query + w)
                # self.cursor.execute("UPDATE user_ids SET id = '123', handler = 'func' WHERE id='1234'")
                self.conn.commit()


        except Exception as e:
            print('ERROR: ', e)
            em.new_error()

    def remove_table_obj(self, this, obj):
        table_name = this.__class__.__name__
        print('REMOVE TABLE NAME: ', table_name)

        try:
            with self.lock:
                query = ""

                # for var, value in obj.__dict__.items():
                #     print(var, value)

                w_id, w_value = next(iter(obj.__dict__.items()))
                w = " WHERE " + str(w_id) + " = " + "'" + str(w_value) + "'"
                print(w)

                self.cursor.execute("DELETE FROM " + table_name + w)
                self.conn.commit()

                #DELETE FROM Customers WHERE CustomerName='Alfreds Futterkiste';

        except Exception as e:
            print('ERROR: ', e)
            em.new_error()

    def migrate(self, obj):
        table_name = obj.__class__.__name__

        table_keys = []
        obj_keys = []

        with self.lock:
            self.cursor.execute("PRAGMA table_info(" + table_name + ")")
            result = self.cursor.fetchall()

            for item in result:
                table_keys.append(item[1])

            for key in obj.__dict__.keys():
                if key != '_list':
                    obj_keys.append(key)

            diff_keys = list(set(obj_keys) - set(table_keys))

            if self.debug:
                print("DIFF: ", diff_keys)

            try:
                for key in diff_keys:
                    self.cursor.execute("ALTER TABLE " + table_name + " ADD COLUMN '%s' 'text'" % key)
            except:
                print('WARNING: table not found')


class TableObject(object):
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


class TableList:

    class _innerObject:
        def __str__(self):
            return str(self.__dict__)

        def __getitem__(self, key):
            return self.__dict__[key]

    def __getitem__(self, key):
        return self._list[key]

    def __len__(self):
        return len(self._list)

    # def save(self):
    #     sql_orm.save_table(self)

    def init(self):
        self._list = []

        sql_orm.migrate(self)
        result = sql_orm.read_table_list(self)

        user_keys = []

        for key in self.__dict__.keys():
            if key != '_list':
                user_keys.append(key)

        def exists_factory(key):
            def func(self, exist_key):
                for obj in self._list:
                    if obj[key] == exist_key:
                        return True
                return False
            return func

        for key in user_keys:
            f = exists_factory(key)
            setattr(TableList, 'exists_' + key, f)

        for item in result:
            i = 0
            _inner_object = TableList._innerObject()

            for key in self.__dict__.keys():
                if key != '_list':
                    _inner_object.__dict__[key] = ''
            for key in user_keys:

                _inner_object.__dict__[key] = item[i].replace(':::', "'")
                
                i += 1

            self._list.append(_inner_object)
        

    def append(self, obj):
        sql_orm.add_table_obj(self, obj)
        self.init()

    def item(self):
        class Item: pass
        item = Item()

        for key in self.__dict__.keys():
            if key != '_list':
                item.__dict__[key] = ''

        return item

    def set(self, obj):
        sql_orm.edit_table_obj(self, obj)

    def remove(self, obj):
        sql_orm.remove_table_obj(self, obj)

    # def save(self):
    #     sql_orm.save_table(self)

    # def __del__(self):
    #     self.save()



sql_orm = SQLLiteOrm(debug=False)

sql_orm.run()

#USAGE EXAMPLE:
# class Car(TableObject):
#     def __init__(self):
#         self.some_var = '4'
#         self.init()


# class cpptest(TableList):
#     def __init__(self):
#         self.q = ''
#         self.answer = ''
#         self.correct = ''
#         self.image = ''
#         self.notes = ''
#         self.init()


# class math_test(TableList):
#     def __init__(self):
#         self.q = ''
#         self.answer = ''
#         self.some_data = ''
#         self.notes = ''
#         self.init()

# cpptest_table = cpptest()
# mtest = math_test()

# for item in cpptest_table:
#     print(item)

# cpptest_table.m()
# for item in mtest:
#     print(item)

# item = mtest.item()

# item.q = 'rara'
# item.answer = '1111'
# item.some_data = '9999'

# mtest.append(item)
