#!/usr/bin/python3

#sudo docker pull scrapinghub/splash
#sudo docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash

import time
import datetime
import requests
from bs4 import BeautifulSoup
import sqlalchemy
from sqlalchemy import create_engine
from random import choice
import pprint

startTime = datetime.datetime.now()

user_agents = [
    'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Debian/1.6-7',
    'Konqueror/3.0-rc4; (Konqueror/3.0-rc4; i686 Linux;;datecode)',
    'Opera/9.52 (X11; Linux i686; U; en)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; it; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13 GTB7.1'
]


def remove_protocol(string):
    string_replaced = string\
        .replace('http://', '')\
        .replace('https://', '')\
        .replace('www.', '')\
        .replace('//', '')
    return string_replaced


def scrape(url):

    params = {"url": url, "wait": 0.3, "with_timeout": 30}
    random_user_agent = choice(user_agents)
    headers = {'User-Agent': random_user_agent}

    try:
        response = requests.get('http://localhost:8050/render.har', params=params, headers=headers, timeout=30)
        status_code = response.status_code
        encoding = response.encoding
        text = response.text
    except requests.exceptions.ReadTimeout:
        status_code = 0
        encoding = ''
        text = ''
        pass

    pprint.pprint(text)


if __name__ == '__main__':

    urls = [
        'piwik.de',
        'bild.de',
        'google.de',
        'facebook.de',
        'web.de',
        'gmx.de',
        'stern.de',
        'spiegel.de',
        't-online.de'
    ]

    for url in urls:
        runTime = datetime.datetime.now()
        result = scrape('http://' + url)
        print('-' * 50)
        print(str(runTime - startTime) + ' | ' + url)
        #pprint.pprint(result)


