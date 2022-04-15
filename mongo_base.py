import os
from mongoengine import *

from pymongo import MongoClient
from pprint import pprint
from bson.objectid import ObjectId

#pip3 install mongoengine
#sudo systemctl start mongod
#pytest -rA

#TODO: add method for saving database to file

#TODO: generate add method with self.schema parameters

#TODO: generate remove methods from self.schema parameters


CHECK_SERVICE_BEFORE_START = True

def runMongoService():
    if not isMongoServiceRun():
        print("Mongo service is not run. Trying to run it...")
        os.system("sudo systemctl start mongod")
        print("Mongo service is run.")

def isMongoServiceRun():
    if CHECK_SERVICE_BEFORE_START:
        try:
            client = MongoClient('localhost', 27017)
            client.server_info()
            return True
        except:
            return False
    else:
        return True

runMongoService()

#Generated methods for lists:
# add_ - add new element to list
# remove_ - remove element from list
# get_ - get list
# print_ - print list

class MongoBaseCache:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[self.__class__.__name__]

        def add_factory(list_name):
            def func(self, value):
                self.push(list_name, value)
            return func

        def remove_factory(list_name):
            def func(self, value):
                self.remove_from_list(list_name, value)
            return func

        def print_factory(list_name):
            def func(self):
                self.print_list(list_name)
            return func

        def get_factory(list_name):
            def func(self):
                return self.get_list(list_name)
            return func

        def update_factory(schema_value_name):
            def func(self, key_value, task_name, value):
                self.update_value(key_value, schema_value_name, task_name, value)
            return func

        def remove_item_factory(schema_value_name):
            def func(self, key_value, task_name):
                self.remove_item(key_value, schema_value_name, task_name)
            return func

        if self.lists:
            for list_name in self.lists:
                f = add_factory(list_name)
                r = remove_factory(list_name)
                p = print_factory(list_name)
                g = get_factory(list_name)

                setattr(MongoBaseCache, 'add_' + list_name, f)
                setattr(MongoBaseCache, 'remove_' + list_name, r)
                setattr(MongoBaseCache, 'print_' + list_name, p)
                setattr(MongoBaseCache, 'get_' + list_name, g)

        if self.schema:
            for schema_value_name in self.schema:
                f = update_factory(schema_value_name)
                setattr(MongoBaseCache, 'update_' + schema_value_name, f)

                f = remove_item_factory(schema_value_name)
                setattr(MongoBaseCache, 'remove_' + schema_value_name, f)

    def remove_item(self, key_value, schema_value_name, task_name):
        self.db.posts.update_one({self.key_value: key_value}, {'$pull': {self.value_key: {schema_value_name: task_name}}})
    
    def update_value(self, key_value, schema_value_name, task_name, value):
        self.db.posts.find_and_modify(
                query = {self.key_value: key_value, ''+ self.value_key + '.' + self.schema[0] : task_name},
                update = { "$set": {self.value_key + '.$.' + schema_value_name : value} }
            )
    
    def _get_list(self, list_name):
        if not self.list_key:
            self.list_key = 'list_name'
        result = self.db.posts.find({self.list_key : list_name})
        try:
            return result[0]
        except:
            return None

    def get_list(self, list_name):
        result = []
        obj = self._get_list(list_name)

        if not self.value_key:
            self.value_key = 'values'

        try:
            for value in obj[self.value_key]:
                result.append(value)
        except:
            pass
        return result

    def print_list(self, list_name):
        print(self.get_list(list_name))

    def remove_from_list(self, list_name, value):
        if type(value) is str:
            if self.findListValue(list_name, value):
                self.db.posts.update_one({'list_name': list_name}, {'$pull': {'values': value}})
        else:
            if self.findListValueObject(list_name, value):
                temp_index = None

                for value_key in value.keys():
                    if type(value_key) is str:
                        temp_index = value_key
                        break

                print('list_name', list_name)
                print('self.value_key: ', self.value_key)
                print('temp_index: ', temp_index)
                print('value[value_key]: ', value[value_key])

                self.db.posts.update_one({self.list_key: list_name}, {'$pull': {self.value_key : {temp_index : value[temp_index]}}})

    def push(self, list_name, value):
        if self.listExists(list_name) == 'NOT_FOUND':
            if not hasattr(self, 'value_key'):
                self.value_key = 'values'
            if not hasattr(self, 'list_key'):
                self.list_key = 'list_name'

            obj = {
                self.value_key: [value],
                self.list_key: list_name
            }
            posts = self.db.posts
            result = posts.insert_one(obj)
            print('Post one: {0}'.format(result.inserted_id))
        else:
            self.update_list(list_name, value)

    def update_list(self, list_name, value):
        if type(value) is str:
            if not self.findListValue(list_name, value):
                print('value in list was not found')

                self.db.posts.update_one({'list_name': list_name}, {'$push': {'values': value}})
        else:
            if not self.findListValueObject(list_name, value):
                print('obj was not found in list')

                self.db.posts.update_one({self.list_key: list_name}, {'$push' : {self.value_key: value}})

    def findListValueObject(self, list_name, obj):
        result = self.db.posts.find({self.list_key: list_name})

        for item in result:
            for internal_item in item[self.value_key]:
                if internal_item == obj:
                    return True
        return False
                # print(internal_item)

    def findListValue(self, list_name, value):
        result = self.db.posts.find({'list_name': list_name})

        for item in result:
            for list_value in item['values']:
                if list_value == value:
                    return True
        return False


    def listExists(self, list_name):
        result = self.db.posts.find({self.list_key : list_name})
        length = result.count()

        if length == 1:
            return 'FOUND'
        elif length == 0:
            return 'NOT_FOUND'
        else:
            return 'ERROR'

    def findValue(self, list_name, value):
        result = self.db.posts.find({list_name : value})

        print(result)
        # return True
        # return False

    def add(self, key_value, obj):
        if self.alreadyExists(key_value) == 'NOT_FOUND':
            post_data = {}

            for key in obj.__dict__.keys():
                if key in self.schema:
                    post_data[key] = getattr(obj, key)
                else:
                    print(key, ' is not in schema')

            posts = self.db.posts

            pprint(post_data)

            obj = {
                self.value_key : [post_data],
                self.key_value : key_value
            }

            if len(post_data):
                result = posts.insert_one(obj)
                print('One post: {0}'.format(result.inserted_id))
        else:
            self._update(key_value, obj)

    def _find_object(self, key_value, obj):
        result = self.db.posts.find({self.key_value: key_value})

        for item in result:
            for task in item[self.value_key]:
                if task[self.schema[0]] == getattr(obj, self.schema[0]):
                    return True
        return False

    def _update(self, key_value, obj):
        if not self._find_object(key_value, obj):
            json_update = {}

            for key in obj.__dict__.keys():
                if key in self.schema:
                    json_update[key] = getattr(obj, key)

            self.db.posts.update_one({self.key_value: key_value}, {'$push': {self.value_key: json_update}})

    def _schema_len_check(self, obj, cached_obj):
        cached_object_schema_count = len(cached_obj.keys()) - 1
        object_schema_count = 0

        for key in obj.__dict__.keys():
            if key in self.schema:
                object_schema_count += 1

        return (cached_object_schema_count == object_schema_count)

    def alreadyExists(self, key_value):
        result = self.db.posts.find({self.key_value : key_value})
        length = result.count()

        if length == 1:
            return 'FOUND'
        elif length == 0:
            return 'NOT_FOUND'
        else:
            return 'ERROR'

    def get(self, key_value):
        try:
            result = self.db.posts.find({self.key_value : key_value})
            return result[0]
        except:
            return None

    def print(self):
        cursor = self.db.posts.find({})
        for document in cursor: 
            pprint(document)

    def size(self):
        return self.db.posts.find({}).count()

    def drop(self):
        self.db.posts.drop()

    def empty(self):
        class Obj: pass

        obj = Obj()

        for key in self.schema:
            setattr(obj, key, None)
            # print('KEY in SCHEMA:', key)

        return obj

    def remove_id(self, idd):
        self.db.posts.remove({'_id': ObjectId(idd)})

    def remove(self, key_value):
        if type(key_value) is str:
            self.db.posts.remove({self.key_value : key_value})
        elif type(key_value) is dict:
            self.db.posts.remove({self.key_value : key_value[self.key_value]})
        else:
            self.db.posts.remove({self.key_value : getattr(key_value, self.key_value)})



class TempCache(MongoBaseCache):
    def __init__(self):
        self.key_value = 'shortcode'
        self.exists_check = 'likes_count'
        self.schema = ['shortcode', 'likes_count', 'test2']
        MongoBaseCache.__init__(self)


class cached_accounts(MongoBaseCache):
    def __init__(self):
        self.key_value = 'username'
        self.exists_check = 'followers_count'
        self.schema = ['username', 'followers_count', 'avarage_like']
        MongoBaseCache.__init__(self)



class cached_photos(MongoBaseCache):
    def __init__(self):
        self.key_value = 'shortcode'
        self.exists_check = 'likes_count'
        self.schema = ['username', 'shortcode', 'likes_count', 
            'real_likes_count', 'likers', 'location_city', 'location_country']
        MongoBaseCache.__init__(self)


class last_check(MongoBaseCache):
    def __init__(self):
        self.key_value = 'username'
        self.exists_check = 'username'
        self.schema = ['username', 'followers', 'followings']
        MongoBaseCache.__init__(self)


class calendar(MongoBaseCache):
    def __init__(self):
        self.key_value = ''
        self.exists_check = 'username'
        self.schema = []
        self.list_key = 'date_code'
        self.value_key = 'tasks'
        self.lists = ['bad_message', 'week_backlog']
        MongoBaseCache.__init__(self)


class some_lists(MongoBaseCache):
    def __init__(self):
        self.key_value = 'username'
        self.exists_check = 'username'
        self.schema = []
        self.lists = ['list1', 'list2', 'list3']
        MongoBaseCache.__init__(self)


class students(MongoBaseCache):
    def __init__(self):
        self.key_value = 'username'
        self.exists_check = 'username'
        self.schema = ['username', 'followers', 'followings']
        self.lists = ['additional_work']
        MongoBaseCache.__init__(self)




# obj = some_lists()
# obj = calendar()

# o = {
#     'task_name': 'test_task2',
#     'done': False
# }
# obj.remove_week_backlog(o)

# obj.print_week_backlog()

# obj.add_list3('asd')
# print(dir(obj))


# obj = last_check()
# # obj.print()


# test_object = obj.empty()
# test_object.username = '_lozai'
# test_object.rara = '123'

# print(dir(test_object))

# print('is exists:', obj.alreadyExists(test_object))


