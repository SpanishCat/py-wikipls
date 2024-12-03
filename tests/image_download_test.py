import time

from src.wikipls import *
import requests
from urllib.parse import urlencode

a = Article("Volcano")
p = a.get_page(TEST_DATE)

with open("media_download_test.png", 'wb') as f:
    f.write(get_image(p.media[0]))

exit()



# Working
h = {
    'User-Agent': 'MediaWiki REST API docs examples/0.1 (https://www.mediawiki.org/wiki/API_talk:REST_API)'
}

o = "Jamiroquai_2018_Coachella18W1-121_%2827188172187%29.jpg"
p = "File:Jamiroquai_2018_Coachella18W1-121_(27188172187).jpg"

p = p.removeprefix("File:")
p = urllib.parse.quote(p)
print(p)
print(o)
print(time.perf_counter())
r = requests.get('https://upload.wikimedia.org/wikipedia/commons/b/b4/' + p
                 , headers=HEADERS)
print(time.perf_counter())

# print(r.url)
# print(r.content)








# print(get_image("Jamiroquai"))

# print(get_media_details("Jamiroquai"))
# print(f"\n{get_image('Jamiroquai').url}")
# get_image("Jamiroquai")
# with open("jam.jpg", 'wb') as f:
#     f.write(get_image("Jamiroquai"))
#
# print(a.key)

# print(a.id)
# print(a.get_page(TEST_DATE).id)
# print(a.get_page(date.today()).id)

# print(get_views("Water", TEST_DATE))
# print(get_views("Water", "20241101"))
