from mongo_base import MongoBaseCache

class test_some_lists(MongoBaseCache):
    def __init__(self):
        self.key_value = 'username'
        self.exists_check = 'username'
        self.schema = ['username', 'password']
        self.lists = ['list1', 'list2', 'list3']
        MongoBaseCache.__init__(self)

#TODO: check if list exists
#TODO: check if exists not added value

class TestMongoBaseCache:
    def test_if_list1_add_method_exists(self):
        obj = test_some_lists()
        assert hasattr(obj, 'add_list1')

    def test_if_list2_add_method_exists(self):
        obj = test_some_lists()
        assert hasattr(obj, 'add_list2')

    def test_if_list3_add_method_exists(self):
        obj = test_some_lists()
        assert hasattr(obj, 'add_list3')

    def test_if_list1_remove_method_exists(self):
        obj = test_some_lists()
        assert hasattr(obj, 'remove_list1')

    def test_if_list2_remove_method_exists(self):
        obj = test_some_lists()
        assert hasattr(obj, 'remove_list2')

    def test_if_list3_remove_method_exists(self):
        obj = test_some_lists()
        assert hasattr(obj, 'remove_list3')

    def test_if_list1_print_method_exists(self):
        obj = test_some_lists()
        assert hasattr(obj, 'print_list1')

    def test_if_list2_print_method_exists(self):
        obj = test_some_lists()
        assert hasattr(obj, 'print_list2')

    def test_if_list3_print_method_exists(self):
        obj = test_some_lists()
        assert hasattr(obj, 'print_list3')

    def test_if_list1_get_method_exists(self):
        obj = test_some_lists()
        assert hasattr(obj, 'get_list1')

    def test_if_list2_get_method_exists(self):
        obj = test_some_lists()
        assert hasattr(obj, 'get_list2')

    def test_if_list3_get_method_exists(self):
        obj = test_some_lists()
        assert hasattr(obj, 'get_list3')

    def test_list_exists_false(self):
        obj = test_some_lists()
        assert obj.listExists('list4') == 'NOT_FOUND'

    def test_list_exists_true(self):
        obj = test_some_lists()
        obj.push('list1', 'value1')
        assert obj.listExists('list1') == 'FOUND'

    def test_find_list_value_false(self):
        obj = test_some_lists()
        obj.push('list1', 'value1')
        assert obj.findListValue('list1', 'value2') == False

    def test_find_list_value_true(self):
        obj = test_some_lists()
        obj.push('list1', 'value1')
        assert obj.findListValue('list1', 'value1') == True

    def test_size_is_zero(self):
        obj = test_some_lists()
        obj.drop()
        assert obj.size() == 0

    def test_size_is_one(self):
        obj = test_some_lists()
        test_value = obj.empty()
        test_value.username = 'test'
        test_value.password = 'test'
        obj.add(test_value)
        assert obj.size() == 1

    def test_size_is_two(self):
        obj = test_some_lists()
        test_value = obj.empty()
        test_value.username = 'test2'
        test_value.password = 'test2'
        obj.add(test_value)
        assert obj.size() == 2

    def test_same_value_is_not_added(self):
        obj = test_some_lists()
        obj.drop()
        test_value = obj.empty()
        test_value.username = 'test'
        test_value.password = 'test'
        obj.add(test_value)
        obj.add(test_value)
        assert obj.size() == 1

    def test_get_method_true(self):
        obj = test_some_lists()
        test_value = obj.empty()
        test_value.username = 'test'
        test_value.password = 'test'
        obj.add(test_value)
        assert obj.get('test')['username'] == 'test'
        assert obj.get('test')['password'] == 'test'

    def test_get_method_false(self):
        obj = test_some_lists()
        test_value = obj.empty()
        test_value.username = 'test'
        test_value.password = 'test'
        obj.add(test_value)
        assert obj.get('test')['username'] != 'test2'
        assert obj.get('test')['password'] != 'test2'

    def test_empty_method(self):
        obj = test_some_lists()
        test_value = obj.empty()
        assert hasattr(test_value, 'username')
        assert hasattr(test_value, 'password')

    def test_already_exists_true(self):
        obj = test_some_lists()
        obj.drop()
        test_value = obj.empty()
        test_value.username = 'test'
        test_value.password = 'test'
        obj.add(test_value)
        assert obj.alreadyExists(test_value) == 'UP_TO_DATE'

    def test_already_exists_false(self):
        obj = test_some_lists()
        obj.drop()
        test_value = obj.empty()
        test_value.username = 'test'
        test_value.password = 'test'
        assert obj.alreadyExists(test_value) == 'NOT_FOUND'

    def test_remove_zero_size(self):
        obj = test_some_lists()
        obj.drop()
        test_value = obj.empty()
        test_value.username = 'test'
        test_value.password = 'test'
        obj.add(test_value)
        obj.remove(test_value)
        assert obj.size() == 0

    def test_remove_one_size(self):
        obj = test_some_lists()
        obj.drop()
        test_value = obj.empty()
        test_value.username = 'test'
        test_value.password = 'test'
        test_value2 = obj.empty()
        test_value2.username = 'test2'
        test_value2.password = 'test2'
        obj.add(test_value)
        obj.add(test_value2)
        obj.remove(test_value)
        assert obj.size() == 1

    def test_drop(self):
        obj = test_some_lists()
        obj.drop()



# obj = test_some_lists()
# obj.push('list1', 'value1')
    