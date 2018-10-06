from hashlib import sha256
from bs4 import BeautifulSoup
import time, datetime, base64, hmac, requests, urllib, xmltodict, json
import collections 
from config import AmazonConfig
def amazon(s):
    access_key_id = AmazonConfig.access_key_id
    secret_key = AmazonConfig.secret_key
    endpoint = AmazonConfig.endpoint
    uri = "/onca/xml"
    payload = collections.OrderedDict(
    [('AWSAccessKeyId', access_key_id),
     ('AssociateTag', 'bookpro3301-21'),
     ('Keywords', s),
     ('Operation', 'ItemSearch'),
     ('ResponseGroup', 'Images,ItemAttributes,Offers'),
     ('SearchIndex', 'Books'),
     ('Service', 'AWSECommerceService'),
     ('Sort', 'relevancerank'),
     ('Timestamp',datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%SZ')),
    ])
    canonical_querystring = urllib.parse.urlencode(payload).replace('+', '%20')
    string_to_sign = "GET\n" + endpoint + "\n" + uri + "\n" + canonical_querystring
    print (string_to_sign)
    dig = hmac.new( bytes(secret_key,'ascii'), msg=bytes(string_to_sign, 'ascii'), digestmod=sha256)
    sig = base64.b64encode(dig.digest())
    print (sig)
    payload['Signature'] = sig
    r = requests.get("http://" + endpoint + uri, params=payload)
    data_dict = xmltodict.parse(r.text)

    if not 'ItemSearchResponse' in data_dict:
        return None

    if 'Errors' in data_dict['ItemSearchResponse']['Items']['Request']:
        return None

    # with open('amazon_data.json', 'w') as f:
    #     json.dump(data_dict, f, indent=4)

    data = data_dict['ItemSearchResponse']['Items']['Item']
    comp = []
    for product in data:
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
        comp.append({
            'title': title,
            'author': author,
            'offer_link': offer_link,
            'link': product['DetailPageURL'] if 'DetailPageURL' in product else '',
            'image': image,
            'price': price,
            'ISBN': ISBN,
            'provider': 'https://images-na.ssl-images-amazon.com/images/G/01/SellerCentral/legal/amazon-logo_transparent.png'
        })
    return comp

if __name__ == "__main__":
	amazon("masala")
