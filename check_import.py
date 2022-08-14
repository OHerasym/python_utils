import subprocess
import sys
from custom_logger import logger


def autoimport(package_name):
    """Import missed python package"""
    try:
        __import__(package_name)
    except ModuleNotFoundError as e:
        logger.error(e)
        logger.info('Trying to install ' + package_name + ' package')

        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])

        __import__(package_name)
        logger.info('Package '+ package_name + ' is installed')



autoimport('pyvirtualdisplay')
autoimport('selenium')
autoimport('seleniumwire')
