"""Module for scanning system values"""
import shutil
import platform
from uuid import getnode as get_mac
import getpass
import socket
import time
import threading
from datetime import datetime
import psutil
from custom_logger import logger


class SystemValue:
    """Class for getting system values"""
    def __init__(self):
        pass

    def cpu(self):
        """Get CPU usage"""
        cpu = psutil.cpu_percent(interval=1)
        logger.debug('CPU: %s', str(cpu))
        return cpu

    def ram(self):
        """Get RAM usage"""
        ram = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
        logger.debug('RAM: %s', str(int(ram)))
        return int(ram)

    def hdd(self):
        """Get HDD usage"""
        total, used, free = shutil.disk_usage("/")
        logger.debug('Total HDD: {} GiB'.format((total // (2**30))))
        logger.debug("Used HDD: {} GiB".format(used // (2**30)))
        logger.debug('Free HDD: {} GiB'.format((free // (2**30))))
        return free // (2**30)

    def sockets(self):
        """Get sockets count"""
        result = psutil.net_connections()
        logger.debug('SOCKETS: %s', str(len(result)))
        return len(result)

    def _lan(self):
        old_value = 0

        while True:
            new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

            if old_value:
                self.lan(new_value)

            old_value = new_value

            time.sleep(1)

    def convert_to_gbit(self, value):
        """Convert bits to Gbit"""
        return value/1024./1024./1024.*8

    def lan(self, value):
        """Print lan data"""
        print("%0.3f" % self.convert_to_gbit(value))


class SystemScanner:
    """Class for scanning system for System Values"""
    def __init__(self, func, cpu=None, ram=None, hdd=None, sockets=None):
        self._thread = None
        self.stop_thread = False
        self.system_value = SystemValue()
        self.callback = func
        self.cpu_value = cpu
        self.ram_value = ram
        self.hdd_value = hdd
        self.sockets_value = sockets
        self.time_period = {}
        self.time_period['CPU'] = 0
        self.time_period['RAM'] = 0
        self.time_period['HDD'] = 0
        self.time_period['SOCKETS'] = 0
        self.info()

    def _check(self, value, user_value, check_type, less=False):
        if value:
            condition = None
            if less:
                condition = user_value < value
            else:
                condition = user_value > value
            if condition:
                self.time_period[check_type] += 1
                if self.time_period[check_type] >= 4:
                    logger.warning(str(check_type) + ' alert!!!!')
                    self.callback(check_type, user_value)
                    self.time_period[check_type] = 0
            else:
                self.time_period[check_type] = 0

    def _check_less(self, value, user_value, check_type):
        self._check(value, user_value, check_type, True)

    def _thread_func(self):
        while not self.stop_thread:
            cpu = None
            ram = None
            hdd = None
            sockets = None

            if self.cpu_value:
                cpu = self.system_value.cpu()
            if self.ram_value:
                ram = self.system_value.ram()
            if self.hdd_value:
                hdd = self.system_value.hdd()
            if self.sockets_value:
                sockets = self.system_value.sockets()

            self._check(self.cpu_value, cpu, 'CPU')
            self._check_less(self.ram_value, ram, 'RAM')
            self._check_less(self.hdd_value, hdd, 'HDD')
            self._check(self.sockets_value, sockets, 'SOCKETS')

            time.sleep(4)


    def scan(self):
        self._thread = threading.Thread(target=self._thread_func)
        self._thread.start()
        logger.info('Start SystemScanner')

    def stop(self):
        self.stop_thread = True
        logger.info('Stopping SystemScanner')

    def info(self):
        logger.info('USERNAME: %s', getpass.getuser())
        logger.info('IP address: %s', socket.gethostbyname(socket.gethostname()))
        logger.info('MAC address: ' + ':'.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2)))
        logger.info('OS: %s', platform.platform())
        boot_time = str(datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S'))
        logger.info('Server boot time: %s', boot_time)


if __name__ == '__main__':
    obj = SystemValue()

    # obj.cpu()
    # obj.ram()
    # obj.hdd()
    # obj.sockets()
    # obj._lan()

    def alert_func(alert_type, value):
        print('alert happened: ', alert_type, value)

    obj = SystemScanner(alert_func, ram=70, cpu=10)
    obj.scan()

    # time.sleep(10)
    # obj.stop()
