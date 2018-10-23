import requests
from threading import Thread
from bs4 import BeautifulSoup


class Snapdeal(Thread):
    def __init__(self, query):
        super(Snapdeal, self).__init__()
        self.query = query
        self.items = []

    def parse_product(self, product):
        data = {'title': product.find('p', {"class": "product-title"}).text,
                'author': '',
                'offer_link': '',
                'link': product.find('a', {"class": "dp-widget-link"})['href'],
                'price': float(product.find('span', {"class": "lfloat product-price"})['display-price']),
                'ISBN': '',
                'provider': 'https://logos-download.com/wp-content/uploads/2016/10/SnapDeal_logo_Snap_Deal.png'}

        try:
            image = product.find('img', {"class": "product-image"})['src']
        except KeyError:
            image = product.find('img', {"class": "product-image"})['data-src']

        if product.find("p", {"class": "product-author-name"}):
            data['author'] = product.find("p", {"class": "product-author-name"}).text
        data['image'] = image
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