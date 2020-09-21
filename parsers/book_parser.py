import re

from locators.locators import Locators


class BookParser:
    Ratings = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    def __init__(self, parent):
        self.parent = parent

    def __repr__(self):
        return f'<{self.title}, £{self.price} (rating: {self.rating})>'

    @property
    def title(self):
        return self.parent.select_one(Locators.TITLE_LOCATOR).attrs['title']

    @property
    def link(self):
        return self.parent.select_one(Locators.TITLE_LOCATOR).attrs['href']

    @property
    def price(self):
        price_str = self.parent.select_one(Locators.PRICE_LOCATOR).string
        pattern = '^£([0-9]+\.[0-9]+)'
        matcher = re.search(pattern, price_str)
        return float(matcher.group(1))

    @property
    def rating(self):
        classes = self.parent.select_one(Locators.RATING_LOCATOR).attrs['class']
        rating = (e for e in classes if e != 'star-rating')
        return BookParser.Ratings.get(next(rating))
