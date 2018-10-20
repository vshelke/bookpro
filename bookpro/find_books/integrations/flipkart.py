import requests, json
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

    def run(self):
        r = requests.get(self.endpoint, params=self.params, headers=self.headers)
        data_dict = json.loads(r.text)

        if len(data_dict['products']) <= 0:
            return None

        products = data_dict['products']
        for product in products:
            title = ''
            author = ''
            ISBN = ''
            offer_link = ''
            image = ''
            price = None
            link = ''
            if 'productBaseInfoV1' in product:
                base = product['productBaseInfoV1']
                title = base['title'] if 'title' in base else ''
                link = base['productUrl'] if 'productUrl' in base else ''
                if 'imageUrls' in base:
                    image = base['imageUrls']['400x400'] if '400x400' in base['imageUrls'] else ''
                if 'flipkartSpecialPrice' in base and base['flipkartSpecialPrice']:
                    price = float(base['flipkartSpecialPrice']['amount']) if 'amount' in base['flipkartSpecialPrice'] else None
                if 'offers' in base:
                    offer_link = base['offers'] if len(base['offers']) > 0 else ''
            if 'categorySpecificInfoV1' in product:
                base2 = product['categorySpecificInfoV1']
                if 'booksInfo' in base2:
                    author = ','.join(base2['booksInfo']['authors']) if 'authors' in base2['booksInfo'] else ''
                if 'keySpecs' in base2:
                    ISBN = '<br>'.join(base2['keySpecs'])
            self.items.append({
                'title': title,
                'author': author,
                'offer_link': offer_link,
                'link': link,
                'image': image,
                'price': price,
                'ISBN': ISBN,
                'provider': 'https://www.underconsideration.com/brandnew/archives/flipkart_logo_detail.jpg'
            })