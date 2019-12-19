#on server install firefox, xorg, openbox, x11-utils

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from custom_logger import logger

def get_browser(use_profile=False):
  browser = None
  if not use_profile:
    binary = FirefoxBinary('/usr/bin/firefox')
    browser = webdriver.Firefox(firefox_binary=binary)
  else:
    ffprofile = webdriver.FirefoxProfile('/home/oleh/.mozilla/firefox/80p26oye.default')
    browser = webdriver.Firefox(ffprofile)
  return browser

class Browser:
  def __init__(self, hide_browser, use_profile=False):
    self.display = Display(visible=0,size=(1024,768))
    if hide_browser:
      self.display.start()
    self.browser = get_browser(use_profile)
    logger.info('init browser')

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

  def switch_window(self, num):
      self.browser.switch_to.window(self.browser.window_handles[num])
 
  def close(self):
    self.browser.close()

  def close_display(self):
    self.display.stop()
    logger.info('close virtual display')

