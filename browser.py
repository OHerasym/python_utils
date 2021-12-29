#on server install firefox, xorg, openbox, x11-utils

#pip3 install selenium
#pip3 install selenium-wire

#install geckodriver
#https://selenium-python.com/install-geckodriver

from pyvirtualdisplay import Display
from selenium import webdriver
import seleniumwire.webdriver as ajax_driver #import webdriver  # Import from seleniumwire
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from custom_logger import logger
import pickle


def get_browser():
  binary = FirefoxBinary('/usr/bin/firefox')
  browser = webdriver.Firefox(firefox_binary=binary)
  logger.debug('default firefox is used')
  return browser

def get_profile_browser():
  ffprofile = webdriver.FirefoxProfile('/home/oleh/.mozilla/firefox/80p26oye.default')
  browser = webdriver.Firefox(ffprofile)
  logger.debug('firefox profile is used')
  return browser

def get_ajax_browser():
  binary = FirefoxBinary('/usr/bin/firefox')
  browser = ajax_driver.Firefox(firefox_binary=binary)
  logger.debug('AjaxBrowser is used')
  return browser

class Browser:
  def __init__(self, hide_browser=False):
    self.display = Display(visible=0,size=(1024,768))
    if hide_browser:
      self.display.start()
    self.browser = self.init_browser()
    logger.info('init browser')

  def init_browser(self):
    return get_browser()

  def load_page(self, page, wait=1):
    self.browser.get(page)
    return self

  def get_page(self):
    return self.browser.page_source

  def wait(self, seconds):
    self.browser.implicitly_wait(seconds)

  def click(self, path):
    elem = self.browser.find_element_by_xpath(path).click()
  
  def clear(self, field):
    elem = self.browser.find_element_by_name(field).clear()

  def edit(self, field, data):
    elem = self.browser.find_element_by_name(field).send_keys(data)

  def elem(self, path):
    return self.browser.find_element_by_xpath(path)

  def switch_window(self, num):
      self.browser.switch_to.window(self.browser.window_handles[num])
 
  def close(self):
    logger.info('close browser')
    self.browser.close()

  def close_display(self):
    self.display.stop()
    logger.info('close virtual display')


class HiddenBrowser(Browser):
  def __init__(self):
    super().__init__(True)


class ProfileBrowser(Browser):
  def __init__(self, hidden=False):
    super().__init__(hidden)

  def init_browser(self):
    return get_profile_browser()


class HiddenProfileBrowser(ProfileBrowser):
  def __init__(self):
    super().__init__(True)


class AjaxBrowser(Browser):
  def __init__(self, hidden=False):
    super().__init__(hidden)

  def init_browser(self):
    return get_ajax_browser()

  def read_cookies(self):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
      self.browser.add_cookie(cookie)

  def write_cookies(self):
    pickle.dump( self.browser.get_cookies() , open("cookies.pkl","wb"))

  def requests(self):
    return self.browser.requests

class HiddenAjaxBrowser(AjaxBrowser):
  def __init__(self):
    logger.info('HiddenAjaxBrowser init')
    super().__init__(True)


# obj = AjaxBrowser()

# obj = Browser(True)
