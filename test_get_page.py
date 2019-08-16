import urllib.request
import urllib.parse
import time
import json
from datetime import datetime

#TODO: if photo/video has less than 7 days, show warning about likes
#TODO: calculate in which time account post photos or videos
#TODO: calculate days of the week when account post photos
#TODO: in which time people comment edges????
#TODO: TOP 10 likers
#TODO: TOP 10 commenters

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

    def _get_graph_image_object(self, edge):
        text = ''
        if len(edge['node']['edge_media_to_caption']['edges']):
            text = edge['node']['edge_media_to_caption']['edges'][0]['node']['text']

        timestamp = edge['node']['taken_at_timestamp']
        dt_object = time.ctime(timestamp)

        photo_data = {
            'likes' : edge['node']['edge_media_preview_like']['count'],
            'url' : edge['node']['display_url'],
            'comments_count' : edge['node']['edge_media_to_comment']['count'],
            'timestamp' : dt_object,
            'text' : text
        }
        return photo_data

    def _get_graph_video_object(self, edge):
        text = ''
        if len(edge['node']['edge_media_to_caption']['edges']):
            text = edge['node']['edge_media_to_caption']['edges'][0]['node']['text']

        timestamp = edge['node']['taken_at_timestamp']
        dt_object = time.ctime(timestamp)

        data = {
            "likes" : edge['node']['edge_media_preview_like']['count'],
            # "url" : edge['node']['video_url'],
            "url" : edge['node']['display_url'],
            "video_view_count" : edge['node']['video_view_count'],
            "comments_count" : edge['node']['edge_media_to_comment']['count'],
            "timestamp" : dt_object,
            "text" : text
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
        self.username_id = self.get_id_by_username(username)
        total_edges = self.get_total_edges(username)
        print('Total edges = ', total_edges)

        if self.is_page_private(username):
            print('Page ' + username + ' is private!')
            return

        page = self.get_page('https://www.instagram.com/' + username + '/')

        first_page_json = self._get_first_page_json(page)
        
        self._parse_edges(first_page_json['user']['edge_owner_to_timeline_media']['edges'])

        cursor = self.get_cursor(page)
        print('cursor = ', cursor)

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
            print(like)

        print('\n\nTOP 10 LOW LIKES VIDEOS')
        for like in self.likes[:10]:
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




obj = PageAnalytics()

obj.analyze('alkhimov_viktor')
