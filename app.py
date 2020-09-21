import aiohttp
import async_timeout
import asyncio
import time
import requests
import logging

from pages.catalog import Catalog


async def fetch_page(session, url):
    page_start = time.time()
    async with async_timeout.timeout(15):
        async with session.get(url) as response:
            logger.info(f'{url} took {time.time() - page_start} seconds to load.')
            return await response.text()


async def get_multiple_pages(loop, *urls):
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:
        for url in urls:
            tasks.append(fetch_page(session, url))
        grouped_tasks = asyncio.gather(*tasks)
        return await grouped_tasks

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M-%S',
                    level=logging.INFO,
                    filename='logs.txt')

logger = logging.getLogger('scraping')

logger.info('Loading books list started...')
page_content = requests.get('http://books.toscrape.com').content
page = Catalog(page_content)

loop = asyncio.get_event_loop()

catalog = []

urls = [f'http://books.toscrape.com/catalogue/page-{page_num}.html' for page_num in range(1, page.page_count + 1)]
pages = loop.run_until_complete(get_multiple_pages(loop, *urls))
logger.info('Loading books list finished...')

for page_content in pages:
    page = Catalog(page_content)
    catalog.extend(page.books)
