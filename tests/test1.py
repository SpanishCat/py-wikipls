import src.wikipy_python as wikipy
import requests
from bs4 import BeautifulSoup

# p = wikipy.WikiPage("Hamas")

# r = requests.get("https://en.wikipedia.org/api/rest_v1/page/title/Hamas").content
# print(r)
with open("test_pdf.pdf", 'wb') as f:
    f.write(wikipy.get_pdf("Jamiroquai"))
# print(wikipy.get_pdf("Hamas"))

# segments = wikipy.get_segments("Hamas")
# # print(segments)
# # exit()
# html = BeautifulSoup(segments)
# print(html.prettify())