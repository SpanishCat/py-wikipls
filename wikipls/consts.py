from datetime import date
from typing import Final

LANG: Final = "en"
TEST_DATE: Final = date(2024, 11, 1)

# HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64"}  # todo Check wiki's docs and change headers
HEADERS: Final = {
    'User-Agent': 'MediaWiki REST API docs examples/0.1 (https://www.mediawiki.org/wiki/API_talk:REST_API)'
}
