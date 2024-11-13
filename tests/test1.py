from src.wikipy_python import *

a = Article("Faded_(Alan_Walker_song)")

print(a.id)
print(a.get_page(TEST_DATE).id)
print(a.get_page(date.today()).id)