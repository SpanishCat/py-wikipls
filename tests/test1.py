from src.wikipls import *

a = Article("Faded_(Alan_Walker_song)")
p = a.get_page(TEST_DATE)

print(p.content_model)
#
# print(a.title)

# print(a.id)
# print(a.get_page(TEST_DATE).id)
# print(a.get_page(date.today()).id)

# print(get_views("Water", TEST_DATE))
# print(get_views("Water", "20241101"))
