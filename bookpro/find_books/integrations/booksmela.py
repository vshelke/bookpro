import requests
from bs4 import BeautifulSoup
from threading import Thread


class BooksMela(Thread):

    def __init__(self, query):
        super(BooksMela, self).__init__()
        self.query = query
        self.items = []

    def check(self, element):
        return '' if element is None else element

    def parse_product(self, product):
        data = {
            'title': '',
            'author': '',
            'offer_link': '',
            'link': '',
            'image': '',
            'price': None,
            'ISBN': '',
            'provider': 'data:image/webp;base64,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'
        }
        data['title'] = self.check(product.find(
            "h2", {"class": "product-name"}).get_text())
        data['author'] = self.check(product.find(
            "span", {"class": "abc-author"}).get_text())
        data['link'] = self.check(product.find(
            "h2", {"class": "product-name"}).a["href"])
        data['image'] = self.check(product.find("img")["src"])
        price = self.check(product.find(
            "span", {"class": "price"}).get_text().strip())
        try:
            data['price'] = float(''.join(filter(str.isdigit, price)))
        except:
            data['price'] = None
        try:
            data['ISBN'] = link.split('-')[-1]
        except:
            data['ISBN'] = None
        print(data)
        return data

    def run(self):
        url = 'https://www.booksmela.com/catalogsearch/result/?q=' + self.query
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        products = soup.findAll("li", {"class": "item last"})
        if len(products) <= 0:
            return None
        for product in products:
            self.items.append(self.parse_product(product))
