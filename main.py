import asyncio
import time
from bs4 import BeautifulSoup
import aiohttp
import logging
from db import Database
from config import DB_NAME, DB_HOST, DB_USER, DB_PASSWORD, urls, headers, cookies

logging.basicConfig(level=logging.DEBUG, filename="metall.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")

loop = asyncio.new_event_loop()

db = Database(loop)

data = dict()

start_time = time.time()


async def get_page_data(session, name):
    url = urls[name]
    header = headers[name]
    cookie = cookies[name]
    async with session.get(url=url, headers=header, cookies=cookie) as response:
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


async def metkom():
    soup = data['METKOM']
    table = soup.find(class_='table catalog-table__table')
    alltr = table.findAll('tr')
    category_id = int
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
                category_id = 9
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
            if await db.metal_exist(name):
                await db.update_metal(name, 3, price)
            else:
                await db.create_metal(category_id, name, price, '', 3, 1, '')


async def vtorchermet():
    soup = data['VTORCHERMET']
    table = soup.find(class_='editorElement layer-type-block ui-droppable block-28').find('article').find('table') \
        .find('tbody')
    alltr = table.findAll('tr')

    for tr in alltr[1:]:
        tds = tr.findAll('td')
        name = tds[0].text.strip()
        price = tds[1].text.strip()
        try:
            price = int(price)
        except:
            price = 0
        if 'МЕДЬ' in name:
            vtor_category_id = 1
        elif 'Бронзы' in name:
            vtor_category_id = 3
        elif 'Лат' in name:
            vtor_category_id = 4
        elif 'Нихром' in name:
            vtor_category_id = 19
        elif 'Титана' in name:
            vtor_category_id = 21
        else:
            vtor_category_id = 19
        if await db.metal_exist(name):
            await db.update_metal(name, 4, price)
        else:
            await db.create_metal(vtor_category_id, name, price, '', 4, 1, '')

    vtor_category_id = 2
    for tr in alltr[1:]:
        tds = tr.findAll('td')
        name = tds[2].text.strip()
        price = tds[3].text.strip()
        try:
            price = int(price)
        except:
            price = 0
        if await db.metal_exist(name):
            await db.update_metal(name, 4, price)
        else:
            await db.create_metal(vtor_category_id, name, price, '', 4, 1, '')

    for tr in alltr[1:]:
        tds = tr.findAll('td')
        name = tds[4].text
        try:
            price = int(tds[5].text)
        except:
            price = 0
        if 'Банки алюм' in name:
            vtor_category_id = 2
        elif 'Нерж' in name:
            vtor_category_id = 9
        elif 'ЦАМ авто' in name:
            vtor_category_id = 15
        elif 'Свинец' in name:
            vtor_category_id = 6
        elif 'АКБ' in name:
            vtor_category_id = 5
        if await db.metal_exist(name):
            await db.update_metal(name, 4, price)
        else:
            await db.create_metal(vtor_category_id, name, price, '', 4, 1, '')


async def cslk():
    soup = data['CSLK']
    med = soup.find(class_='price--color price-block').find(class_='price__card-accordion price__card-accordion--el') \
        .findAll(class_='accordion-line')
    for i in range(1, len(med)):
        name = med[i].find(class_='price__card-name').text
        price = med[i].find(class_='price__card-coast--730').text.strip().split('/')
        try:
            price = float(price[1])
        except:
            price = 0
        if 'Медь' in name or 'Медная' in name:
            category_id = 1
        elif 'Латун' in name:
            category_id = 4
        elif 'Алюм' in name or 'Офсетный лист' in name:
            category_id = 2
        elif 'Титан' in name:
            category_id = 21
        elif 'ЦАМ' in name:
            category_id = 15
        elif 'Магний' in name:
            category_id = 20
        elif 'Нержавейка' in name:
            category_id = 9
        elif 'электродвигат' in name:
            category_id = 1
        elif 'нихром' in name:
            category_id = 19
        elif 'Бронза' in name:
            category_id = 3
        else:
            category_id = 0

        if await db.metal_exist(name):
            await db.update_metal(name, 5, price)
        else:
            await db.create_metal(category_id, name, price, '', 5, 1, '')


async def vtormet():
    soup = data['VTORMET']
    med = soup.find(class_='price2').find('tbody').findAll('tr')
    for i in range(len(med)):
        tds = med[i].findAll('td')
        if len(tds) == 1:
            continue
        for td in range(0, len(tds), 2):
            try:
                name = tds[td].text.strip().replace(u'\xa0', '')
                price = tds[td + 1].text.strip()
                try:
                    price = float(price)
                except:
                    price = 0
                if 'меди' in name:
                    category_id = 1
                elif 'бронз' in name:
                    category_id = 3
                elif 'латун' in name:
                    category_id = 4
                elif 'алюмин' in name:
                    category_id = 2
                elif 'ЦАМ' in name:
                    category_id = 15
                elif 'магни' in name:
                    category_id = 20
                elif 'нержавеющ' in name:
                    category_id = 9
                elif 'свинц' in name:
                    category_id = 6
                elif 'аккум' in name:
                    category_id = 5
                elif 'нихром' in name:
                    category_id = 19
                elif 'вольфрам' in name:
                    category_id = 18
                elif 'титан' in name:
                    category_id = 12
                else:
                    category_id = 19
                if await db.metal_exist(name):
                    await db.update_metal(name, 6, price)
                else:
                    await db.create_metal(category_id, name, price, '', 6, 1, '')
            except:
                continue


async def main():
    await gather_data()
    await db.connect(host=DB_HOST, port=3306, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
    await metkom()
    await vtorchermet()
    await cslk()
    await vtormet()
    finish_time = time.time() - start_time
    logging.info(f"Затраченное на работу скрипта время: {finish_time}")


if __name__ == "__main__":
    loop.run_until_complete(main())
