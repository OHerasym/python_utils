# from pytube import YouTube

# YouTube('https://www.youtube.com/watch?v=vPvUtmKGNyM').streams.first().download('.')


from urllib.request import urlopen
import requests
import time




class RandomImage:
    def __init__(self):
        pass

    def _save_image(self, image_name, pic_url):
        with open(image_name, 'wb') as handle:
                response = requests.get(pic_url, stream=True)

                if not response.ok:
                    print(response)

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)


    def get(self, count):
        while count:
            html = urlopen("http://www.funcage.com/?").read().decode('utf-8')

            start_str = '<a href="/funnypicture.php?image=photos/'
            result_end = html[html.find(start_str) + len(start_str):].find('"')
            image_name = html[html.find(start_str) + len(start_str):html.find(start_str) + len(start_str) + result_end]

            print("http://www.funcage.com/photos/" + image_name)
            self._save_image(image_name, "http://www.funcage.com/photos/" + image_name)

            count -= 1


r = RandomImage()
r.get(3)
