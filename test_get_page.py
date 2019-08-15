import urllib.request
import urllib.parse
import time
import json

#TODO: add photos parsing
#TODO: add total edges count
#TODO: create top 10 photo likes
#TODO: create top 10 video likes


class PageAnalytics:
    def __init__(self):
        self.username_id = ''


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




    def analyze(self, username):
        self.username_id = self.get_id_by_username(username)

        page = self.get_page('https://www.instagram.com/' + username + '/')

        cursor = self.get_cursor(page)
        #get total edges count
        #get text from json

        likes = []
        photo_likes = []

        for i in range(0, 10):
            time.sleep(3)
            
            try:
                page = self.get_page('https://www.instagram.com/graphql/query/?' + self.prepare_params(cursor))
                json_page = json.loads(page)
            except:
                print('Request error')
                break

            for edge in json_page['data']['user']['edge_owner_to_timeline_media']['edges']:
                try:
                    if edge['node']['__typename'] == 'GraphImage':
                        photo_data = {
                            'likes' : edge['node']['edge_media_preview_like']['count'],
                        }
                        print(photo_data)
                        photo_likes.append(photo_data)

                    elif edge['node']['__typename'] == 'GraphVideo':
                        data = {
                            "likes" : edge['node']['edge_media_preview_like']['count'],
                            "url" : edge['node']['video_url'],
                            "video_view_count" : edge['node']['video_view_count'],
                            "comments_count" : edge['node']['edge_media_to_comment']['count'],
                            "timestamp" : edge['node']['taken_at_timestamp'],
                            # "text" : edge['node']['edge_media_to_caption']['edges']['node']['text']
                        }

                        print(data)
                        likes.append(data)
                    else:
                        print('__typename = ', edge['node']['__typename'])
                except:
                    print('Some parse error')
                    print(edge)
                    time.sleep(10000)

            cursor = json_page['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']


        likes.sort(key=lambda x:x['likes'])
        photo_likes.sort(key=lambda x:x['likes'])


        print('PHOTO LIKES')

        for like in photo_likes:
            print(like)

        print('\n\n\nVIDEO LIKES')
        for like in likes:
            print(like)




obj = PageAnalytics()

obj.analyze('alkhimov_viktor')