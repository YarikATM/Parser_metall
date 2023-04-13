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
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/'
              '*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ru,en;q=0.9',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Yandex";v="22"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/102.0.5005.167 YaBrowser/22.7.5.1018 Yowser/2.5 Safari/537.36',
}

cookies_METKOM = {
    '_ym_uid': '1681263721804668417',
    '_ym_d': '1681263721',
    '_ga_QNH4166XCD': 'GS1.1.1681263721.1.0.1681263721.0.0.0',
    '_ga': 'GA1.1.432438949.1681263721',
}

headers_VTORCHERMET = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    }

cookies_VTORCHERMET = {
    'stats': '1',
    'onc-5c2364a6b887eeef6d8b4672-user-id': '6437e3dd5008acd7368b5019',
    'onc-5c2364a6b887eeef6d8b4672-user-hash': '7b3b06db94c4d6c5a1cc66fe47f93f95',
}

headers_CSLK = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
                }

cookies_CSLK = {}

headers_VTORMET = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',}

cookies_VTORMET = {'aa8d2adcbb6e5689ba4cb431e0b3fd99': 'nv0munilnbu9664afvlkhrnii7',
    'adtech_uid': '1a2b4dae-12ed-4b59-b78f-a766105bcd18^%^3Axn--24-dlcm8alooe.xn--p1ai',
    'top100_id': 't1.2689957.762878688.1681384305689',
    't3_sid_2689957': 's1.283098244.1681384305690.1681384305693.1.2',
    'last_visit': '1681359105690^%^3A^%^3A1681384305690',
    '_ym_uid': '1681384306575066342',
    '_ym_d': '1681384306',
    '__utma': '196464101.252347396.1681384306.1681384306.1681384306.1',
    '__utmb': '196464101.1.10.1681384306',
    '__utmc': '196464101',
    '__utmz': '196464101.1681384306.1.1.utmcsr=(direct)^|utmccn=(direct)^|utmcmd=(none)',
    '__utmt': '1',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
                   }

headers = {'METKOM': headers_METKOM, 'VTORCHERMET': headers_VTORCHERMET,
           'CSLK': headers_CSLK, 'VTORMET': headers_VTORMET}

cookies = {'METKOM': cookies_METKOM, 'VTORCHERMET': cookies_VTORCHERMET,
           'CSLK': cookies_CSLK, 'VTORMET': cookies_VTORMET}