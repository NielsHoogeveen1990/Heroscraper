import requests
import re

from bs4 import BeautifulSoup

BASE_URL = 'https://psionic-storm.com/en/heroes/'


def get_re_url(soup, pattern):
    return [url.get('href') for url in soup.find_all('a') if re.search(pattern, url.get('href'))]

def url_to_soup(url):
    page = requests.get(url).content
    soup = BeautifulSoup(page, 'html.parser')
    return soup


def get_data_units(hero_soup, name):
    return hero_soup.find('span', attrs={'data-units': name}).get_text().strip()


def get_release_date(hero_soup):
    descrip = hero_soup.find('div', attrs={'class': 'hero-description'}).get_text().strip()
    try:
        return re.findall(r'\d{4}-\d{2}-\d{2}', descrip)[0]
    except IndexError:
        return None


def get_hero_info(url):
    hs = url_to_soup(url)
    try:
        return {
            'name': hs.find('h1').get_text(),
            'health points': get_data_units(hs, 'hp'),
            'damage per attack': get_data_units(hs, 'aa-dmg'),
            'attack speed': get_data_units(hs, 'aa-speed'),
            'mana': get_data_units(hs, 'mana'),
            'damage per second': get_data_units(hs, 'aa-dps'),
            'gold price': hs.find('span', attrs={'class': 'price-gold'}).get_text().strip(),
            'attack range': get_data_units(hs, 'aa-range'),
            'hero type': hs.find('p', attrs={'class': 'hero-subtitle'}).get_text().strip(),
            'release date': get_release_date(hs),
        }
    except AttributeError:
        print(f'Error for hero {name_from_url(url)}')


def name_from_url(url):
    return url.split('/')[-2]


def get_hero_urls():
    main_page_soup = url_to_soup(BASE_URL)
    hero_urls = get_re_url(main_page_soup, pattern='com/en/heroes/.+')
    return hero_urls


def scrape_all(n=None):
    hero_urls = get_hero_urls()

    if n is not None:
        hero_urls = hero_urls[:n]

    hero_info = {name_from_url(url): get_hero_info(url) for url in hero_urls}

    return hero_info


def scrape_hero(hero_name):
    hero_url = BASE_URL + hero_name
    hero_info = get_hero_info(hero_url)

    return hero_url, hero_info


if __name__ == '__main__':
    pass
