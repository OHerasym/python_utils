import urllib.request
from html.parser import HTMLParser
from threading import Thread
import time

import telegram

# url_page = 'https://www.olx.ua/nedvizhimost/arenda-pomescheniy/arenda-restoranov-barov/odessa/'
url_page = 'https://www.olx.ua/nedvizhimost/odessa/'


class TelegramBot:
	def __init__(self):
		self._bot = telegram.Bot(token='467894598:AAFvPlPP_aEW0GKhafBcXxdjanEzucTUuoo')

	def send_message(self, message):
		chat_id = self._bot.get_updates()[-1].message.chat_id
		self._bot.send_message(chat_id=chat_id, text=message)


class GlobalData:
	_data = []

	def merge_data(data):
		if data == None:
			return
		for data1 in data:
			if data1 in GlobalData._data:
				continue
			else:
				GlobalData._data.append(data1)

	def get_diff(data):
		if data == None:
			return None

		diff_list = []
		for data1 in data:
			if data1 in GlobalData._data:
				continue
			else:
				diff_list.append(data1)
		return diff_list


class DataRent:
	def __init__(self):
		self.uans = []
		self.urls = []
		self.titles = []
		self.last_tag_img = False
		self.is_href = 0
		self.is_uan_checked = False

	def _is_data_correct(self):

		if 'https://www.olx.ua' == self.urls[0]:
			del self.urls[0]

		if len(self.titles) == len(self.urls) + 1:
			del self.titles[0]

		print(len(self.uans))
		print(len(self.urls))
		print(len(self.titles))

		# print(self.uans)
		# print(self.urls)
		# print(self.titles)
		_error = False
		if len(self.uans) == len(self.urls) == len(self.titles):
			return True

		self.uans = self.uans[:-len(self.uans) - 5]
		self.urls = self.urls[:-len(self.urls) - 5]
		self.titles = self.titles[:-len(self.titles) - 5]

		print('[ERROR]: trying to fix data')

		return True

	def clean(self):
		del self.uans[:]
		del self.urls[:]
		del self.titles[:]

data_rent = DataRent()

class MyHTMLParser(HTMLParser):
	def handle_data(self, data):
		if data_rent.is_href == 1:
			data_rent.is_href = 2
			return

		if data_rent.is_href == 2:
			data_rent.is_href = 0
			data_rent.titles.append(data)

		if ' грн' in data and data_rent.is_uan_checked:
			data_rent.uans.append(data)
			data_rent.is_uan_checked = False

	def handle_starttag(self, tag, attrs):
		if tag == 'img':
			data_rent.last_tag_img = True

		if tag == 'a':
			for name, value in attrs:
				if name == 'href' and data_rent.last_tag_img:
					data_rent.urls.append(value) 
					data_rent.last_tag_img = False
					data_rent.is_href = 1
					data_rent.is_uan_checked = True


class PageReader:
	def __init__(self, url):
		self._data_rent = DataRent()
		self._page = None
		self._url = url

	def get_data(self):
		self._page = urllib.request.urlopen(self._url).read().decode('utf-8')
		print(self._page)
		parser = MyHTMLParser()
		parser.feed(self._page)
		if not data_rent._is_data_correct():
			print('[ERROR]: Data is not correct')

			return None

		_list = []

		for a, b, c in zip(data_rent.titles, data_rent.uans, data_rent.urls):
			_list.append([a, b, c])
	
		return _list



class PageChecker:
	def __init__(self):
		self._page_reader = PageReader(url_page)
		self._exit = False
		self._bot = TelegramBot()
		self._first_iteration = True

	def _checker_thread(self, dummy):
		while True:
			print('Iteration')
			# time.sleep(10)

			# _diff = GlobalData.get_diff(self._page_reader.get_data())

			# self._page_reader.get_data()

			# print('Diff: ', _diff)
			data_rent.clean()

			# if _diff == None:
				# continue


			# if self._first_iteration:
			# 	self._first_iteration = False
			# else:
			# 	for obj in _diff:
			# 		print('Title: ', obj[0])
			# 		print('Вартість: ', obj[1])
			# 		print('link: ', obj[2])
			# 		self._bot.send_message(obj[0] + '\nЦіна: ' + obj[1])
			# 		# time.sleep(3)
			# 		# self._bot.send_message('Ціна: ' + obj[1])
			# 		time.sleep(3)
			# 		self._bot.send_message('Лінк: ' + obj[2])

			# GlobalData.merge_data(_diff)


			if self._exit:
				break


	def run(self):
		checker = Thread(target=self._checker_thread, args=(10,))
		checker.start()

		input()
		self._exit = True


p  = PageReader(url_page)

p.get_data()
# page_checker = PageChecker()
# page_checker.run()