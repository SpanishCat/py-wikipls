# What is this?
Wikipls is a Python package meant to easily scrape data out of Wikipedia (maybe more of the Wikimedia in the future), using the REST API.
This package is still in early development, but it has basic functionality all set.

# Why does it exist?
The REST API for wikimedia, isn't the most intuitive and requires some learning.
When writing code, it also requires setting up a few functions to make it more manageable and readable.
So essentially I made these functions and packaged them so that you (and I) won't have to rewrite them every time.
While I'm at it I made them more intuitive and easy to use without needing to figure out how this API even works.

# Installation
To install use: `pip install py_wikipls`

# How to use
I haven't made any documentation page yet, so for now the below will have to do.\
If anything is unclear don't hesitate to open an issue in [Issues](https://github.com/SpanishCat/py-wikipls/issues).

  ## Key
  Many functions in this package require the name of the Wiki page you want to check in a URL-friendly format.
  The REST documentation refers to that as a the "key" of an article.
  For example: 
  - The article titled "Water" is: "Water"
  - The article titled "Faded (Alan Walker song)" is: "Faded_(Alan_Walker_song)"
  - The Article titled "Georgia (U.S. state)" is: "Georgia_(U.S._state)"

  That key is what you enter in the *name* parameter of functions.

  To get the key of an article you can:
  1. Take a look at the url of the article.\
    The URL for "Faded" for example is "https://en.wikipedia.org/wiki/Faded_(Alan_Walker_song)".
    Notice it ends with "wiki/" followed by the key of the article.
  2. Take the title of the article and replace all spaces with "_", it'll probably work just fine.
  3. In the future there will be a function to get the key of a title.

  ## Direct Functions
  These functions can be used without needing to create an object. 
  In general they all require the URL-friendly name of an article as a string.
  
  ### get_views(name: str, date_: str | date, lang: str = LANG) -> int
  returns the number of times people visited an article on a given date.
  
  

# Bug reports
This package is in early development and I'm looking for community feedback on bugs.\
If you encounter a problem, please report it in [Issues](https://github.com/SpanishCat/py-wikipls/issues).

# What does the name mean?
Wiki = Wikipedia
Pls = Please, because you make requests

# Versions
This version of the package is written in Python. I plan to eventually make a copy of this one written in Rust (using PyO3 and maturin).
Why Rust? It's an exercise for me, and it will be way faster and less error-prone

# Plans
- Support for revisions (i.e. the ability to get an older version of an article)
- Support for more languages (Currently supports only English Wikipedia)
- Dictionary
- Citations
