import collections, time, datetime, base64, hmac, requests, urllib, xmltodict, json
from bs4 import BeautifulSoup
from hashlib import sha256
from config import AmazonConfig
from threading import Thread


class Amazon(Thread):
    def __init__(self, query):
        super(Amazon, self).__init__()
        self.query = query
        self.items = []
        self.access_key_id = AmazonConfig.access_key_id
        self.secret_key = AmazonConfig.secret_key
        self.endpoint = AmazonConfig.endpoint
        self.uri = "/onca/xml"

    def get_payload(self):
        payload = collections.OrderedDict([   
            ('AWSAccessKeyId', self.access_key_id),
            ('AssociateTag', 'bookpro3301-21'),
            ('Keywords', self.query),
            ('Operation', 'ItemSearch'),
            ('ResponseGroup', 'Images,ItemAttributes,Offers'),
            ('SearchIndex', 'Books'),
            ('Service', 'AWSECommerceService'),
            ('Sort', 'relevancerank'),
            ('Timestamp', datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%SZ')),
        ])
        canonical_querystring = urllib.parse.urlencode(payload).replace('+', '%20')
        string_to_sign = "GET\n" + self.endpoint + "\n" + self.uri + "\n" + canonical_querystring
        dig = hmac.new( bytes(self.secret_key,'ascii'), msg=bytes(string_to_sign, 'ascii'), digestmod=sha256)
        sig = base64.b64encode(dig.digest())
        payload['Signature'] = sig
        return payload

    def run(self):
        payload = self.get_payload()
        r = requests.get("http://" + self.endpoint + self.uri, params=payload)
        data_dict = xmltodict.parse(r.text)

        if not 'ItemSearchResponse' in data_dict:
            return None

        if 'Errors' in data_dict['ItemSearchResponse']['Items']['Request']:
            return None

        products = data_dict['ItemSearchResponse']['Items']['Item']
        for product in products:
            title = ''
            author = ''
            ISBN = ''
            offer_link = ''
            image = ''
            price = None
            link = ''
            if 'ItemAttributes' in product:
                item = product['ItemAttributes']
                title = item['Title'] if 'Title' in item else ''
                if 'Author' in item:
                    if isinstance(item['Author'], list):
                        author = ', '.join(item['Author'])
                    else:
                        author = item['Author']
                ISBN = item['ISBN'] if 'ISBN' in item else ''
            if 'Offers' in product:
                offer_link = product['Offers']['MoreOffersUrl'] if 'MoreOffersUrl' in product['Offers'] else ''
            if 'LargeImage' in product:
                image = product['LargeImage']['URL'] if 'URL' in product['LargeImage'] else ''
            if 'OfferSummary' in product:
                if 'LowestNewPrice' in product['OfferSummary']:
                    price = float(product['OfferSummary']['LowestNewPrice']['FormattedPrice'][4:].replace(',','')) if 'FormattedPrice' in product['OfferSummary']['LowestNewPrice'] else None
            self.items.append({
                'title': title,
                'author': author,
                'offer_link': offer_link,
                'link': product['DetailPageURL'] if 'DetailPageURL' in product else '',
                'image': image,
                'price': price,
                'ISBN': ISBN,
                'provider': 'https://images-na.ssl-images-amazon.com/images/G/01/SellerCentral/legal/amazon-logo_transparent.png'
            })
