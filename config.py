from dotenv import load_dotenv
import os
import logging

load_dotenv('.env')


try:
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
except (TypeError, ValueError) as ex:
    logging.error("Error while reading config:", ex)


urls = {
    'METKOM': "https://krasnoyarsk.metkom-group.ru/",
    'VTORCHERMET': "https://siblom24.ru/tseny-tsvetnogo-loma",
    'CSLK': "http://cslk24.ru/",
    'VTORMET': 'https://втормет24.рф/ceni/tsvetnoj-lom-po-zonam.html'
}

headers_METKOM = {
    'authority': 'krasnoyarsk.metkom-group.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ru,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': '_ym_uid=1681263721804668417; _ym_d=1681263721; _ga_QNH4166XCD=GS1.1.1681263721.1.0.1681263721.0.0.0; _ga=GA1.1.432438949.1681263721',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Yandex";v="22"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.5.1018 Yowser/2.5 Safari/537.36',
}

cookies_METKOM = {
    '_ym_uid': '1681263721804668417',
    '_ym_d': '1681263721',
    '_ga_QNH4166XCD': 'GS1.1.1681263721.1.0.1681263721.0.0.0',
    '_ga': 'GA1.1.432438949.1681263721',
}
#TODO добавить headers и cookies
headers_VTORCHERMET = {}

cookies_VTORCHERMET = {}

headers_CSLK = {}

cookies_CSLK = {}

headers_VTORMET = {}

cookies_VTORMET = {}

headers = {'METKOM': headers_METKOM, 'VTORCHERMET': headers_VTORCHERMET,
           'CSLK': headers_CSLK, 'VTORMET': headers_VTORMET}

cookies = {'METKOM': cookies_METKOM, 'VTORCHERMET': cookies_VTORCHERMET,
           'CSLK': cookies_CSLK, 'VTORMET': cookies_VTORMET}