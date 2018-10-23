from threading import Thread

import requests
from bs4 import BeautifulSoup


class Snapdeal(Thread):
    def __init__(self, query):
        super(Snapdeal, self).__init__()
        self.query = query
        self.items = []

    def check(self, element):
        return '' if element is None else element

    def parse_product(self, product):
        data = {'author': '',
                'title': '',
                'offer_link': '',
                'link': '',
                'price': None,
                'ISBN': '',
                'provider': 'https://logos-download.com/wp-content/uploads/2016/10/SnapDeal_logo_Snap_Deal.png'}

        if self.check(product.find('p', {"class": "product-title"})):
            data['title'] = product.find('p', {"class": "product-title"}).text
        if self.check(product.find('a', {"class": "dp-widget-link"})):
            data['link'] = product.find('a', {"class": "dp-widget-link"})['href']
        if self.check(product.find('span', {"class": "lfloat product-price"})):
            data['price'] = float(product.find('span', {"class": "lfloat product-price"})['display-price'])
        if self.check(product.find("p", {"class": "product-author-name"})):
            data['author'] = product.find("p", {"class": "product-author-name"}).text
        if self.check(product.find('img', {"class": "product-image"})):
            try:
                data['image'] = product.find('img', {"class": "product-image"})['src']
            except KeyError:
                data['image'] = product.find('img', {"class": "product-image"})['data-src']
        return data

    def run(self):
        url = f'https://www.snapdeal.com/products/books?sort=rlvncy&keyword={self.query}'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        products = soup.findAll(
            "div", {"class": "favDp"})
        if len(products) <= 0:
            return None
        for product in products:
            self.items.append(self.parse_product(product))