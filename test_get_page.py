import urllib.request
import urllib.parse
import time
import json
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import operator

#TODO: in which time people comment edges????

nakrukta_tags = ['#likeforlike', '#followme', '#likeforfollow']

class PageAnalytics:
    def __init__(self):
        self.username_id = ''
        self.likes = []
        self.photo_likes = []


    def get_page(self, url):
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()

        page = mybytes.decode('utf8')
        fp.close()
        return page


    def get_id_by_username(self, username):
        page = self.get_page('https://www.instagram.com/' + username + '/?__a=1')
        json_page = json.loads(page)
        return json_page['graphql']['user']['id']

    def get_total_edges(self, username):
        page = self.get_page('https://www.instagram.com/' + username + '/?__a=1')
        json_page = json.loads(page)
        return json_page['graphql']['user']['edge_owner_to_timeline_media']['count']

    def is_page_private(self, username):
        page = self.get_page('https://www.instagram.com/' + username + '/?__a=1')
        json_page = json.loads(page)
        if json_page['graphql']['user']['is_private']:
            return True
        return False

    def get_biography(self, username):
        page = self.get_page('https://www.instagram.com/' + username + '/?__a=1')
        json_page = json.loads(page)
        return json_page['graphql']['user']['biography']

    def get_followers_count(self, username):
        page = self.get_page('https://www.instagram.com/' + username + '/?__a=1')
        json_page = json.loads(page)
        return json_page['graphql']['user']['edge_followed_by']['count']

    def get_full_name(self, username):
        page = self.get_page('https://www.instagram.com/' + username + '/?__a=1')
        json_page = json.loads(page)
        return json_page['graphql']['user']['full_name']

    def is_business_account(self, username):
        page = self.get_page('https://www.instagram.com/' + username + '/?__a=1')
        json_page = json.loads(page)
        return json_page['graphql']['user']['is_business_account']

    def is_account_verified(self, username):
        page = self.get_page('https://www.instagram.com/' + username + '/?__a=1')
        json_page = json.loads(page)
        return json_page['graphql']['user']['is_verified']

    def get_profile_pic(self, username):
        page = self.get_page('https://www.instagram.com/' + username + '/?__a=1')
        json_page = json.loads(page)
        return json_page['graphql']['user']['profile_pic_url_hd']

    def total_likes(self):
        count = 0
        for edge in self.photo_likes:
            count += edge['likes']
        for edge in self.likes:
            count += edge['likes']
        return count

    def total_comments(self):
        count = 0
        for edge in self.photo_likes:
            count += edge['comments_count']
        for edge in self.likes:
            count += edge['comments_count']
        return count

    def get_top_likers(self):
        result = {}

        for edge in self.photo_likes:
            for liker in edge['likers']:
                if liker in result:
                    result[liker] += 1
                else:
                    result[liker] = 1

        for edge in self.likes:
            for liker in edge['likers']:
                if liker in result:
                    result[liker] += 1
                else:
                    result[liker] = 1

        print('Top likers = ', result)
        sorted_result = sorted(result.items(), key=operator.itemgetter(1))
        print(sorted_result[-10:])

    def get_top_commenters(self):
        result = {}

        for edge in self.photo_likes:
            for comment in edge['comments']:
                if comment['username'] in result:
                    result[comment['username']] += 1
                else:
                    result[comment['username']] = 1

        for edge in self.likes:
            for comment in edge['comments']:
                if comment['username'] in result:
                    result[comment['username']] += 1
                else:
                    result[comment['username']] = 1

        print('Top commenters = ', result)
        sorted_result = sorted(result.items(), key=operator.itemgetter(1))
        print(sorted_result[-10:])


    def posting_time(self):
        result = {}

        for edge in self.photo_likes:
            hour = datetime.fromtimestamp(edge['timestamp']).hour

            if hour in result:
                result[hour] += 1
            else:
                result[hour] = 1

        for edge in self.likes:
            hour = datetime.fromtimestamp(edge['timestamp']).hour

            if hour in result:
                result[hour] += 1
            else:
                result[hour] = 1

        print('POSTING TIME = ', result)

        plt.bar(result.keys(), result.values(), color='g')
        plt.xticks(np.arange(24))
        plt.title('Posting Time')
        plt.show()

    def _weekday_to_string(self, weekday):
        if weekday == 0:
            return 'Monday'
        elif weekday == 1:
            return 'Tuesday'
        elif weekday == 2:
            return 'Wednesday'
        elif weekday == 3:
            return 'Thusday'
        elif weekday == 4:
            return 'Friday'
        elif weekday == 5:
            return 'Saturday'
        else:
            return 'Sunday'

    def weekday_posting(self):
        result = {}
        result['Monday'] = 0
        result['Tuesday'] = 0
        result['Wednesday'] = 0
        result['Thusday'] = 0
        result['Friday'] = 0
        result['Saturday'] = 0
        result['Sunday'] = 0

        for edge in self.photo_likes:
            weekday = datetime.fromtimestamp(edge['timestamp']).weekday()
            weekday = self._weekday_to_string(weekday)

            if weekday in result:
                result[weekday] += 1
            else:
                result[weekday] = 1

        for edge in self.likes:
            weekday = datetime.fromtimestamp(edge['timestamp']).weekday()
            weekday = self._weekday_to_string(weekday)

            if weekday in result:
                result[weekday] += 1
            else:
                result[weekday] = 1

        print('WEEKDAY POSTING = ', result)

        plt.bar(result.keys(), result.values(), color='g')
        plt.xticks(np.arange(7))
        plt.title('Weekday Posting Time')
        plt.show()

    def get_top_hashtags(self):
        edges_hashtags = {}

        for edge in self.photo_likes[-10:]:
            hash_tags = []
            text = edge['text']
            tags = text.split(' ')

            for tag in tags:
                if len(tag) == 0:
                    break
                if tag[0] == '#':
                    if tag in edges_hashtags:
                        edges_hashtags[tag] += 1
                    else:
                        edges_hashtags[tag] = 1

        for edge in self.likes[-10:]:
            hash_tags = []
            text = edge['text']
            tags = text.split(' ')

            for tag in tags:
                if len(tag) == 0:
                    break
                if tag[0] == '#':
                    if tag in edges_hashtags:
                        edges_hashtags[tag] += 1
                    else:
                        edges_hashtags[tag] = 1


        print('Top 10 tags = ', edges_hashtags)

        if any(elem in edges_hashtags for elem in nakrukta_tags):
            print('\n\nWARNING: nakrukta detected!!!!!!')
        # plt.bar(edges_hashtags.keys(), edges_hashtags.values(), color='g')
        # plt.title('Hash tags from TOP 10')
        # plt.show()

        # labels = edges_hashtags.keys()
        # sizes = edges_hashtags.values()
        # fig1, ax1 = plt.subplots()
        # ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        # ax1.axis('equal')
        # plt.show()


    def get_cursor(self, page):
        find_str = '"page_info":{"has_next_page":true,"end_cursor":"'

        start_index = page.find(find_str)

        end_index = page[start_index + len(find_str):].find('"}')

        cursor = page[start_index + len(find_str): start_index + len(find_str) + end_index]
        return cursor


    def prepare_params(self, cursor):
        params = {
            "query_hash" : "f2405b236d85e8296cf30347c9f08c2a",
            "variables" : {
               "id" : self.username_id,
               "first" : 50,
               "after" : cursor
            }
        }

        query_string = urllib.parse.urlencode(params)
        query_string = query_string.replace('+', '').replace('27', '22')
        return query_string

    def prepare_params_for_comments(self, shortcode):
        params = {
            'query_hash' : '477b65a610463740ccdb83135b2014db',
            'variables' : {
                'shortcode' : shortcode,
                'child_comment_count' : 3,
                'fetch_comment_count' : 40,
                'parent_comment_count': 24,
                'has_threaded_comments' : 'true'
            }
        }
        query_string = urllib.parse.urlencode(params)
        query_string = query_string.replace('+', '').replace('27', '22').replace('%22true%22', 'true')
        return query_string

    def prepare_params_for_likers(self, shortcode):
        params = {
            'query_hash' : 'd5d763b1e2acf209d62d22d184488e57',
            'variables' : {
                'shortcode' : shortcode,
                'include_reel' : 'true',
                'first' : 200
            }
        }
        query_string = urllib.parse.urlencode(params)
        query_string = query_string.replace('+', '').replace('27', '22').replace('%22true%22', 'true')
        return query_string

    def get_comments_by_short_code(self, shortcode):
        page = self.get_page('https://www.instagram.com/graphql/query/?' + self.prepare_params_for_comments(shortcode))
        json_page = json.loads(page)

        comments = []

        for comment in json_page['data']['shortcode_media']['edge_media_to_parent_comment']['edges']:
            print(comment['node']['text'])
            print(comment['node']['created_at'])
            print('owner = ', comment['node']['owner']['username'])

            comment = {
                'text' : comment['node']['text'],
                'created_at' : comment['node']['created_at'],
                'username' : comment['node']['owner']['username']
            }
            comments.append(comment)
        return comments

    def get_likers_by_short_code(self, shortcode):
        page = self.get_page('https://www.instagram.com/graphql/query/?' + self.prepare_params_for_likers(shortcode))
        json_page = json.loads(page)

        likers = []

        for liker in json_page['data']['shortcode_media']['edge_liked_by']['edges']:
            likers.append(liker['node']['username'])

        return likers

    def _get_graph_image_object(self, edge):
        text = ''
        comments = []
        if len(edge['node']['edge_media_to_caption']['edges']):
            text = edge['node']['edge_media_to_caption']['edges'][0]['node']['text']

        timestamp = edge['node']['taken_at_timestamp']
        dt_object = timestamp
        # time.sleep(3)
        # likers = self.get_likers_by_short_code(edge['node']['shortcode'])
        if edge['node']['edge_media_to_comment']['count'] > 0:
            time.sleep(3)
            comments = self.get_comments_by_short_code(edge['node']['shortcode'])

        photo_data = {
            'likes' : edge['node']['edge_media_preview_like']['count'],
            'url' : edge['node']['display_url'],
            'comments_count' : edge['node']['edge_media_to_comment']['count'],
            'timestamp' : dt_object,
            'text' : text,
            # 'likers' : likers,
            'comments' : comments
        }

        return photo_data

    def _get_graph_video_object(self, edge):
        text = ''
        if len(edge['node']['edge_media_to_caption']['edges']):
            text = edge['node']['edge_media_to_caption']['edges'][0]['node']['text']

        timestamp = edge['node']['taken_at_timestamp']
        dt_object = timestamp
        # time.sleep(3)
        # likers = self.get_likers_by_short_code(edge['node']['shortcode'])
        time.sleep(3)
        comments = self.get_comments_by_short_code(edge['node']['shortcode'])

        data = {
            "likes" : edge['node']['edge_media_preview_like']['count'],
            # "url" : edge['node']['video_url'],
            "url" : edge['node']['display_url'],
            "video_view_count" : edge['node']['video_view_count'],
            "comments_count" : edge['node']['edge_media_to_comment']['count'],
            "timestamp" : dt_object,
            "text" : text,
            # 'likers' : likers,
            'comments' : comments
        }
        return data

    def _parse_edges(self, edges):
        for edge in edges:
            # try:
                if edge['node']['__typename'] == 'GraphImage':
                    photo_data = self._get_graph_image_object(edge)
                    
                    print(photo_data)
                    self.photo_likes.append(photo_data)

                elif edge['node']['__typename'] == 'GraphVideo':
                    data = self._get_graph_video_object(edge)

                    print(data)
                    self.likes.append(data)
                else:
                    data = self._get_graph_image_object(edge)
                    print(data)
                    self.photo_likes.append(data)
            # except:
                # print('Some parse error')
                # print(edge)
                # time.sleep(10000)

    def _get_first_page_json(self, page):
        find_str = 'window._sharedData = {"config":'

        start_index = page.find(find_str)
        end_index = page[start_index:].find('</script>')

        page_json_only = page[start_index + len('window._sharedData = '): start_index + end_index - 1]
        first_page_json = json.loads(page_json_only)

        return first_page_json['entry_data']['ProfilePage'][0]['graphql']


    def analyze(self, username):
        try:
            self.username_id = self.get_id_by_username(username)
        except:
            print('ERROR: Wrong username')
            return

        total_edges = self.get_total_edges(username)
        print('Total edges = ', total_edges)

        if self.is_page_private(username):
            print('Page ' + username + ' is private!')
            return

        page = self.get_page('https://www.instagram.com/' + username + '/')

        first_page_json = self._get_first_page_json(page)
        
        self._parse_edges(first_page_json['user']['edge_owner_to_timeline_media']['edges'])

        cursor = self.get_cursor(page)

        requests_number = int(total_edges - 12 / 50) + 1

        for i in range(0, requests_number):
            time.sleep(3)
            
            try:
                page = self.get_page('https://www.instagram.com/graphql/query/?' + self.prepare_params(cursor))
                json_page = json.loads(page)
            except:
                print('Request error')
                break

            self._parse_edges(json_page['data']['user']['edge_owner_to_timeline_media']['edges'])

            cursor = json_page['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']



        self.likes.sort(key=lambda x:x['likes'])
        self.photo_likes.sort(key=lambda x:x['likes'])


        print('\n\nTOP 10 LOW LIKES PHOTOS')
        for like in self.photo_likes[:10]:
            dt_object = datetime.fromtimestamp(like['timestamp'])
            diff_time = datetime.now() - dt_object
            if diff_time.days < 7:
                print('WARNING: Posted less than 7 days ago')
            print(like)

        print('\n\nTOP 10 LOW LIKES VIDEOS')
        for like in self.likes[:10]:
            dt_object = datetime.fromtimestamp(like['timestamp'])
            diff_time = datetime.now() - dt_object
            if diff_time.days < 7:
                print('WARNING: Posted less than 7 days ago')
            print(like)

        print('\n\nPHOTOS TOP 10 LIKES')

        for like in self.photo_likes[-10:]:
            print(like)

        print('\n\n\nVIDEO LIKES')
        for like in self.likes[-10:]:
            print(like)

        print('photo count = ', len(self.photo_likes))
        print('video count = ', len(self.likes))
        print('Total likes = ', self.total_likes())
        print('Total comments = ', self.total_comments())
        print('\n\nTotal = ', len(self.photo_likes) + len(self.likes))

        # self.posting_time()
        # self.weekday_posting()
        # self.get_top_hashtags()
        # self.get_top_likers()
        self.get_top_commenters()


obj = PageAnalytics()

# obj.analyze('oolleehh1991')
print(obj.get_biography('oolleehh1991'))
print(obj.get_followers_count('oolleehh1991'))
print(obj.get_full_name('oolleehh1991'))
print(obj.is_business_account('oolleehh1991'))
print(obj.is_account_verified('oolleehh1991'))
print(obj.get_profile_pic('oolleehh1991'))