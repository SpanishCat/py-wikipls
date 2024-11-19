# What is this?
Wikipls is a Python package meant to easily scrape data out of Wikipedia (maybe more of the Wikimedia in the future), using its REST API.
This package is still in early development, but it has basic functionality all set.

# Why does it exist?
The REST API for wikimedia, isn't the most intuitive and requires some learning.
When writing code, it also requires setting up a few functions to make it more manageable and readable.
So essentially I made these functions and packaged them so that you (and I) won't have to rewrite them every time.
While I'm at it I made them more intuitive and easy to use without needing to figure out how this API even works.

# Installation
To install use:\
`pip install py-wikipls`

Then in your code add:\
`import wikipls`

# How to use
I haven't made any documentation page yet, so for now the below will have to do.\
If anything is unclear don't hesitate to open an issue in [Issues](https://github.com/SpanishCat/py-wikipls/issues).\
Updated for version: 0.0.1a5

  ## Key
  Many functions in this package require the name of the Wiki page you want to check in a URL-friendly format.
  The REST documentation refers to that as a the "key" of an article.
  For example: 
  - The key of the article titled "Water" is: "Water"
  - The key of the article titled "Faded (Alan Walker song)" is: "Faded_(Alan_Walker_song)"
  - The key of the Article titled "Georgia (U.S. state)" is: "Georgia_(U.S._state)"

  That key is what you enter in the *name* parameter of functions. **The key is case-sensitive.**

  To get the key of an article you can:
  1. Take a look at the url of the article.\
    The URL for "Faded" for example is "https://en.wikipedia.org/wiki/Faded_(Alan_Walker_song)".
    Notice it ends with "wiki/" followed by the key of the article.
  2. Take the title of the article and replace all spaces with "_", it'll probably work just fine.
  3. In the future there will be a function to get the key of a title.

  ## Direct Functions
  These functions can be used without needing to create an object. 
  In general they all require the URL-friendly name of an article as a string.
  
  ### `get_views(name: str, date: str | datetime.date, lang: str = LANG) -> int`
  Returns the number of times people visited an article on a given date.

  The date given can be either a datetime.date object or a string formatted *yyyymmdd* (So *March 31th 2024* will be *"20240331"*).

  `>>> get_views("Faded_(Alan_Walker_song)", "20240331")`\
  `1144`
  
The Faded page on Wikipedia was visited 1,144 on March 31st 2024.

  
  ### `get_html(name: str) -> str`
  Returns the html of the page as a string. 
  This can be later parsed using tools like BeautifulSoup.

  `>>> get_html("Faded_(Alan_Walker_song)")[:40]`\
  `'<!DOCTYPE html>\n<html prefix="dc: http:/'`

  This example returns the beginning of the html of the "Faded" page.


  ### `get_summary(name: str) -> str`
  Returns a summary of the page.

  `>>> get_summary("Faded_(Alan_Walker_song)")[:120]`\
  `'"Faded" is a song by Norwegian record producer and DJ Alan Walker with vocals provided by Norwegian singer Iselin Solhei'`

  This examples returns the first 120 letters of the summary of the Faded page


  ### `get_media_details(name: str) -> tuple[dict, ...]`
  Returns all media present in the article, each media file represented as a JSON.

`>>> get_media_details("Faded_(Alan_Walker_song)")[0]`\
  `{'title': 'File:Alan_Walker_-_Faded.png', 'leadImage': False, 'section_id': 0, 'type': 'image', 'showInGallery': True, 'srcset': [{'src': '//upload.wikimedia.org/wikipedia/en/thumb/d/da/Alan_Walker_-_Faded.png/220px-Alan_Walker_-_Faded.png', 'scale': '1x'}, {'src': '//upload.wikimedia.org/wikipedia/en/d/da/Alan_Walker_-_Faded.png', 'scale': '1.5x'}, {'src': '//upload.wikimedia.org/wikipedia/en/d/da/Alan_Walker_-_Faded.png', 'scale': '2x'}]}`

  This example returns the first media file in the Faded article, which is a PNG image.

  ### `get_image(details: dict[str, ...]) -> bytes`
  Retrives the actual byte-code of an image on a an article, using a JSON representing the image.
  You can get that JSON using `get_media_details()`.

  `>>> get_image({'title': 'File:Alan_Walker_-_Faded.png', 'leadImage': False, 'section_id': 0, 'type': 'image', 'showInGallery': True, 'srcset': [{'src': '//upload.wikimedia.org/wikipedia/en/thumb/d/da/Alan_Walker_-_Faded.png/220px-Alan_Walker_-_Faded.png', 'scale': '1x'}, {'src': '//upload.wikimedia.org/wikipedia/en/d/da/Alan_Walker_-_Faded.png', 'scale': '1.5x'}, {'src': '//upload.wikimedia.org/wikipedia/en/d/da/Alan_Walker_-_Faded.png', 'scale': '2x'}]})`\
  `b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01,\x00\x00\x01,\x08\x03\x00\x00\x00N\xa3~G\x00\x00\x03\x00PLTE\xff\xff\xff\x01\x01\x01\xfe\xfd\xfe'`

  This examples returns the first bytes of the image we got in the `get_media_details()` example.

  ### `get_all_images(input: str | Iterable[dict[str, ...]], strict: bool = True) -> tuple[bytes]`
  Returns all images of an article or a provided list of image-JSONs, in bytes form.

  ### `get_pdf(name: str) -> bytes`
  Returns the PDF version of the page in byte-form.

  `>>> with open("faded_wiki.pdf", 'wb') as f:`\
  `      f.write(get_pdf("Faded_(Alan_Walker_song)"))`

  This example imports the Faded page in PDF form as a new file named "faded_wiki.pdf".


  ### `get_page_data(name: str, date: str | datetime.date) -> dict`
  Returns details about the latest revision to the page in JSON form.\
  If date is provided, returns the latest revision details as of that date.

  ### `get_article_data(identifier: str | int, lang: str = LANG) -> dict[str, ...]`
  Returns details about an article in JSON form.\
  Identifier can be either the article's name or its ID.

  ### `to_timestamp(date: datetime.date) -> str`
  Converts a datetime.date object or a string in format yyyy-mm-ddThh:mm:ssZ to a URL-friendly string format (yyyymmdd)

  `>>> date = datetime.date(2024, 3, 31)`\
  `>>> to_timestamp(date)`\
  `20240331`

  This example converts the date of March 31th 2024 to URL-friendly string form.

  ### `from_timestamp(timestamp: str) -> datetime.date`
  Converts a timestamp to a datetime.date object.\
  The timestamp is a string which is written in one of the following formats:
  - yyyymmdd
  - yyyy-mm-ddThh:mm:ssZ

  ### `id_of_page(name: str, date: str | datetime.date, lang: str = LANG) -> int`
  Returns an id of a page, given a name.\
  Date argument is optional: If date is provided, returns the ID of latest revision as of that date.

  ### `name_of_page(id: int, lang=LANG) -> str`
  Returns the title (not key!) of an article given its ID.

  ## Class objects  
  If you intend on repeatedly getting info about some page, it is preferred that you make an object for that page.\
  This is for reasons of performance as well as readability and organization.
  
  ### `wikipls.Article(name: str)`
  An "Article" is a wikipedia article in all of its versions, revisions and languages.

  #### Properties
  `.name` (str): Article title.\
  `.key` (str): Article key (URL-friendly name).\
  `.id` (int): Article ID. Doesn't change across revisions.\
  `.content_model` (str): Type of wiki project this article is a part of (e.g. "wikitext", "wikionary").\
  `.license` (dict): Details about the copyright license of the article.\
  `.latest` (dict): Details about the latest revision done to the article.\
  `.html_url` (str): URL to an html version of the current revision of the article.\
  `.details` (dict[str, Any]): All the above properties in JSON form.\
  
  `.get_page(date: datetime.date, lang: str = "en")` (wikipls.Page): Get a Page object of this article, from a specified date and in a specified translation.

  #### Example properties
  -- TODO

  
  ### `wikipls.Page(article: Article, date: datetime.date)`
  A "Page" is a version of an article in a specific date and a specific language, a.k.a a "revision".

  #### Properties
  `.name` (str): Page title.\
  `.key` (str): The key of the page (URL-friendly name).).\
  `.article_id` (int): ID of the article this page is derived from.\
  `.revision_id` (int): ID of the current revision of the article.\
  `.date` (datetime.date): The date of the page.\
  `.lang` (str): The language of the page as an ISO 639 code (e.g. "en" for English).\
  `.content_model` (str): Type of wiki project this page is a part of (e.g. "wikitext", "wikionary").\
  `.license` (dict): Details about the copyright license of the page.\
  `.views` (int): Number of vists this page has received during its specified date.\
  `.html` (str): Page HTML.\
  `.summary` (str): Summary of the page.\
  `.media` (tuple[dict, ...]): All media files in the page represented as JSONs.\
  `.as_pdf` (bytes): The PDF version of the page in bytes-code.\
  `.data` (dict[str, Any]): General details about the page in JSON format.\
  `.article_details` (dict): Details related to the article the page is derived from.\
  `.page_details` (dict): Details related to the current revision of the page.\

  #### Example properties
  -- TODO


# What does the name mean?
Wiki = Wikipedia\
Pls = Please, because you make requests

# Versions
This version of the package is written in Python. I plan to eventually make a copy of this one written in Rust (using PyO3 and maturin).
Why Rust? It's an exercise for me, and it will be way faster and less error-prone

# Plans
- Support for more languages (Currently supports only English Wikipedia)
- Dictionary
- Citations
  
# Bug reports
This package is in early development and I'm looking for community feedback on bugs.\
If you encounter a problem, please report it in [Issues](https://github.com/SpanishCat/py-wikipls/issues).
