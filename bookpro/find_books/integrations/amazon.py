import collections
import time
import datetime
import base64
import hmac
import requests
import urllib
import xmltodict
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
            ('Timestamp', datetime.datetime.fromtimestamp(
                time.time()).strftime('%Y-%m-%dT%H:%M:%SZ')),
        ])
        canonical_querystring = urllib.parse.urlencode(
            payload).replace('+', '%20')
        string_to_sign = "GET\n" + self.endpoint + \
            "\n" + self.uri + "\n" + canonical_querystring
        dig = hmac.new(bytes(self.secret_key, 'ascii'), msg=bytes(
            string_to_sign, 'ascii'), digestmod=sha256)
        sig = base64.b64encode(dig.digest())
        payload['Signature'] = sig
        return payload

    def parse_product(self, product):
        data = {
            'title': '',
            'author': '',
            'offer_link': '',
            'link': product.get('DetailPageURL', ''),
            'image': '',
            'price': None,
            'ISBN': '',
            'provider': 'https://images-na.ssl-images-amazon.com/images/G/01/SellerCentral/legal/amazon-logo_transparent.png'
        }
        item = product.get('ItemAttributes', False)
        offers = product.get('Offers', '')
        image = product.get('LargeImage', '')
        summary = product.get('OfferSummary', '')
        if item:
            data['title'] = item.get('Title', '')
            data['author'] = item.get('Author', '')
            if data['author'] and isinstance(data['author'], list):
                data['author'] = ', '.join(data['author'])
            data['ISBN'] = item.get('ISBN', '')
        if offers:
            data['offer_link'] = offers.get('MoreOffersUrl', '')
        if image:
            data['image'] = image.get('URL', '')
        if summary and summary.get('LowestNewPrice', False):
            if summary['LowestNewPrice'].get('FormattedPrice', False):
                data['price'] = float(summary['LowestNewPrice']
                                      ['FormattedPrice'][4:].replace(',', ''))
        return data

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
            self.items.append(self.parse_product(product))
