import asyncio
import datetime
import time
from bs4 import BeautifulSoup
import aiohttp
import logging
from db import Database
from config import DB_NAME, DB_HOST, DB_USER, DB_PASSWORD

logging.basicConfig(level=logging.INFO, filename="metall.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

db = Database(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

urls = {
    'METKOM': "https://krasnoyarsk.metkom-group.ru/",
    'VTORCHERMET': "https://siblom24.ru/tseny-tsvetnogo-loma",
    'CSLK': "http://cslk24.ru/",
    'VTORMET': 'https://втормет24.рф/ceni/tsvetnoj-lom-po-zonam.html'
}

data = dict()

start_time = time.time()


async def get_page_data(session, name):
    url = urls[name]

    async with session.get(url=url, ) as response:
        if response.status != 200:
            logging.error(url, response.status)
        else:
            response_text = await response.text()

            soup = BeautifulSoup(response_text, "lxml")
            data[name] = soup
            print(f"[INFO] Обработал страницу {url}")


async def gather_data():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        tasks = []

        for name in urls.keys():
            task = asyncio.create_task(get_page_data(session, name))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_data())
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    metkom()
    finish_time = time.time() - start_time
    logging.info(f"Затраченное на работу скрипта время: {finish_time}")


def metkom():
    soup = data['METKOM']
    table = soup.find(class_='table catalog-table__table')
    alltr = table.findAll('tr')
    category = ''
    category_id = int()
    for tr in alltr[1:]:
        if tr.has_attr('class'):
            title = tr.text.strip()
            if title == '':

                pass
            #TODO перевод категории в id
        else:
            block = tr.findAll('td')
            name = block[0].text.strip()
            price = block[1].text.strip()
            print([name, price, category])


if __name__ == "__main__":
    main()
