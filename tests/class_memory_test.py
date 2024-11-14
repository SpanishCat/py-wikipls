import src.wikipls as wikipy
from time import perf_counter

page_key = "Faded_(Alan_Walker_song)"
article = wikipy.Article(page_key)
page = article.get_page(wikipy.TEST_DATE)
a = perf_counter()
print(page.views)
b = perf_counter()
print(page.views)
c = perf_counter()
print(page.views)
d = perf_counter()
print(page.views)
e = perf_counter()
print(page.views)
f = perf_counter()

a *= 1000
b *= 1000
c *= 1000
d *= 1000
e *= 1000
f *= 1000

print(f"a: {b-a}, b: {c-b}, c:{d-c}, d:{e-d}, e:{f-e}")
# print(wikipy.get_views("Faded_(Alan_Walker_song)", wikipy.TEST_DATE))

