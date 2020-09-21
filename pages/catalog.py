import re
import logging
from bs4 import BeautifulSoup

from locators.locators import Locators
from parsers.book_parser import BookParser

logger = logging.getLogger('scraping.catalog')


class Catalog:
    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')

    @property
    def books(self):
        return [BookParser(e) for e in self.soup.select(Locators.BOOK_LOCATOR)]

    @property
    def page_count(self):
        content = self.soup.select_one(Locators.PAGER_LOCATOR).string
        pattern = 'Page [0-9]+ of ([0-9]+)'
        matcher = re.search(pattern, content)
        logger.info(f'Number of catalog pages available: `{matcher.group(1)}`')
        return int(matcher.group(1))
