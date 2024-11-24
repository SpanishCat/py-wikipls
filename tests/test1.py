from src.wikipls import *
from wikipls.consts import TEST_DATE

# a = Article("Faded_(Alan_Walker_song)")
# p = a.get_page(datetime.date(2024, 3, 31))
#

r = get_revision_data("Faded_(Alan_Walker_song)", TEST_DATE)
print(f"{r = }")

# print(p)

# 1223086768 = 9.5.2024

# d = get_page_data(RevisionId(1223086768))
# print(f"{d = }")

# get_article_data(ArticleId(49031279))
# print("\n\n")
# print(key_of_page(ArticleId(49031279)))
