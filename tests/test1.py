from src.wikipls import *

a = Article("Faded_(Alan_Walker_song)")
p = a.get_page(datetime.date(2024, 3, 31))

print(p)

# print(get_page_data("Faded_(Alan_Walker_song)", TEST_DATE))
