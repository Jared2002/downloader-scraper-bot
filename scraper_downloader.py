import requests
import lxml.html as html
import os
from urllib.request import Request, urlopen

HOME_URL = 'https://www.plasticosyresinas.com/catalogo/'
MODIFIER = '?count=36&paged='

XPATH_LINK_TO_SECTION = '//div[@class="col-md-3 sidebar left-sidebar mobile-hide-sidebar"]/aside/ul/li/a/@href'
XPATH_TITLE = '//h1/text()'
XPATH_IMG = '//div[@class="inner"]/img/@src'
XPATH_IMG_NAME = '//a[@class="product-loop-title"]/h2/text()'


def download_images(source, name, folder):
    try:
        i = 0
        x = len(source)
        y = len(name)
        if x == y:
            while(i < x):
                with open(f'{folder}/{name[i]}.jpg', 'wb') as f:
                    req = Request(source[i], headers={
                                  'User-Agent': 'Mozilla/5.0'})
                    f.write(urlopen(req).read())
                    f.close
                i = i + 1
    except ValueError as ve:
        print(ve)


def get_names(link):
    try:
        link = link + MODIFIER
        response = requests.get(link)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            name_img = parsed.xpath(XPATH_IMG_NAME)
            for name in name_img:
                name.lower().replace(' ', '-').replace('.', '_')
            return name_img
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def get_images(link):
    try:
        link = link + MODIFIER
        response = requests.get(link)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            url_img = parsed.xpath(XPATH_IMG)
            return url_img
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def get_title(link):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            title = parsed.xpath(XPATH_TITLE)
            title_format = title[0].lower().replace(' ', '-')
            return title_format
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_section = parsed.xpath(XPATH_LINK_TO_SECTION)

            for link in links_to_section:
                title_format = get_title(link)
                if not os.path.isdir(title_format):
                    os.mkdir(title_format)
                download_images(get_images(link),
                                get_names(link), title_format)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == "__main__":
    run()
