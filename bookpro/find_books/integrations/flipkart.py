import requests
import json
from config import FlipkartConfig
from threading import Thread


class Flipkart(Thread):
    def __init__(self, query):
        super(Flipkart, self).__init__()
        self.query = query
        self.headers = {
            'Fk-Affiliate-Id': FlipkartConfig.aff_id,
            'Fk-Affiliate-Token': FlipkartConfig.token,
        }
        self.params = {
            'query': query + ' book',
            'resultCount': 10,
        }
        self.endpoint = FlipkartConfig.endpoint
        self.items = []

    def parse_product(self, product):
        data = {
            'title': '',
            'author': '',
            'offer_link': '',
            'link': '',
            'image': '',
            'price': None,
            'ISBN': '',
            'provider': 'https://www.underconsideration.com/brandnew/archives/flipkart_logo_detail.jpg'
        }
        base = product.get('productBaseInfoV1', '')
        specific = product.get('categorySpecificInfoV1', '')
        if base:
            data['title'] = base.get('title', '')
            data['link'] = base.get('productUrl', '')
            if 'imageUrls' in base:
                data['image'] = base['imageUrls'].get('400x400', '')
            if base.get('flipkartSpecialPrice', False):
                if base['flipkartSpecialPrice'].get('amount', False):
                    data['price'] = float(
                        base['flipkartSpecialPrice']['amount'])
            if 'offers' in base:
                data['offer_link'] = base['offers'] if len(
                    base['offers']) > 0 else ''
        if specific:
            if 'booksInfo' in specific and specific['booksInfo'].get('authors', False):
                data['author'] = ','.join(specific['booksInfo']['authors'])
            if 'keySpecs' in specific:
                data['ISBN'] = '<br>'.join(specific['keySpecs'])
        return data

    def run(self):
        r = requests.get(self.endpoint, params=self.params,
                         headers=self.headers)
        data_dict = json.loads(r.text)
        if len(data_dict['products']) <= 0:
            return None
        products = data_dict['products']
        for product in products:
            self.items.append(self.parse_product(product))
