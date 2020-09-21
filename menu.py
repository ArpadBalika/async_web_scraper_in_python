import logging

from app import catalog


logger = logging.getLogger('scraping.menu')


def print_best_books():
    best_books = sorted(catalog, key=lambda x: (x.rating * -1, x.price))
    for book in best_books:
        if book.rating == 5:
            print(book)
    logger.info('5-star books listed.')


def print_cheapest_books():
    cheapest_books = sorted(catalog, key=lambda x: x.price)[:10]
    for book in cheapest_books:
        print(book)
    logger.info('10 cheapest books listed.')


book_generator = (b for b in catalog)


def print_next_book():
    print(next(book_generator))


def menu():
    USER_CHOICE = """Menu:

- 'b' list 5 star books
- 'c' list the 10 cheapest books
- 'n' see next available book
- 'q' exit
"""

    functions = {
        'b': print_best_books,
        'c': print_cheapest_books,
        'n': print_next_book
    }

    user_input = input(USER_CHOICE)
    while user_input != 'q':
        if user_input in functions:
            functions[user_input]()
        else:
            print('Invalid input')
        user_input = input(USER_CHOICE)

    logger.info('Quit selected, program terminated')


menu()
