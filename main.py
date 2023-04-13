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
    loop = asyncio.new_event_loop()
    loop.run_until_complete(gather_data())
    loop.run_until_complete(asyncio.sleep(0.250))
    loop.close()

    metkom()

    finish_time = time.time() - start_time
    logging.info(f"Затраченное на работу скрипта время: {finish_time}")


def metkom():
    soup = data['METKOM']
    table = soup.find(class_='table catalog-table__table')
    alltr = table.findAll('tr')
    category_id = int()
    start_time = time.time()
    for tr in alltr[1:]:
        if tr.has_attr('class'):
            title = tr.text.strip()
            if title == 'Прием лома меди':
                category_id = 1
            elif title == 'Прием лома латуни':
                category_id = 4
            elif title == 'Бронза':
                category_id = 3
            elif title == 'Прием лома алюминия':
                category_id = 2
            elif title == 'Прием лома цинка':
                category_id = 15
            elif title == 'Прием лома магния':
                category_id = 20
            elif title == 'Нержавеющая сталь':
                category_id =  9
            elif title == 'Прием лома титана':
                category_id = 21
            elif title == 'Лом черных металлов':
                category_id = 22
            elif title == 'Прием лома никеля':
                category_id = 8
        else:
            block = tr.findAll('td')
            name = block[0].text.strip()
            price = block[1].text.replace('руб', '').strip()
            try:
                price = int(price)
            except:
                price = 0
            if db.metall_exists(name):
                db.update_metall(category_id, name, 3, 1, price)
            else:
                db.create_metall(category_id, name, price, '', 3, 1, '')
            print([name, price,  category_id])
    finish_time = time.time() - start_time
    print(finish_time)

if __name__ == "__main__":
    main()
