#TODO: get all likes and links

from InstagramApi.InstagramAPI import InstagramAPI

users1 = [ 'test1', 'test2', 'test3', 'test4']

users2 = [ 'test1', 'test3', 'test4', 'test5']


print(set(users1) - set(users2))


class InstaAnalytics:
	def __init__(self):
		self.api = InstagramAPI("", "")
		self.api.login()
		self.followers = None

	def _get_followers_list(self):
		self.followers = self.api.getTotalFollowers(self.api.username_id)
		print(len(self.followers))

		followers_names = []

		for follower in self.followers:
			followers_names.append(follower['username'])

		return followers_names

	def _save_followers_list(self):
		f = open('followers1.txt', 'w')

		for follower in self.followers:
			print(follower['username'])
			f.write(follower['username'] + '\n')

		f.close()

	def _get_followers_from_file(self):
		f = open('followers1.txt', 'r')

		file_followers = f.read().split('\n')
		return file_followers

	def followers_diff(self, old_list, new_list):
		print('Unsubscribed followers:')
		print(set(old_list) - set(new_list))
		print('\nNew followers:')
		print(set(new_list) - set(old_list))


	def check(self):
		new_followers = self._get_followers_list()
		old_followers = self._get_followers_from_file()
		self.followers_diff(old_followers, new_followers)


analytics = InstaAnalytics()

analytics.check()