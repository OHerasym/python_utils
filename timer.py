"""Timer module"""

import threading
from threading import Thread
import time
from custom_logger import logger

class Timer:
    """Class for async call func after timeout"""
    def __init__(self, sleep_time, func, single_shot=False):
        self.thread = Thread(target=self._internal_thread)
        self._event = threading.Event()
        self._func = func
        self._result_func = None
        self.sleep_time = sleep_time
        self.single_shot = single_shot

    def set_result_func(self, func):
        """Set result callback"""
        self._result_func = func

    def _internal_thread(self):
        while not self._event.wait(self.sleep_time):
            result = self._func()

            if result:
                if self._result_func:
                    logger.debug('on_result call')
                    self._result_func(result)

            if self.single_shot:
                break

    def start(self):
        """Start timer"""
        self.thread.start()

    def on_exit(self):
        """Stop timer"""
        self._event.set()


if __name__ == '__main__':
    def test_func():
      print('test_func')
      return 42

    def get_result(result):
      print('result: ', result)

    obj = Timer(2, test_func)
    obj.set_result_func(get_result)
    obj.start()

    print('rrara')

    time.sleep(10)
    obj.on_exit()
