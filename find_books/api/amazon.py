from hashlib import sha256
from bs4 import BeautifulSoup
import time, datetime, base64, hmac, requests, urllib, xmltodict, json
import collections

def amazon(s):
    access_key_id = 'AKIAJKBJSCFX6V2ODHAA'
    secret_key = "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"
    endpoint = "webservices.amazon.in"
    uri = "/onca/xml"
    payload = collections.OrderedDict(
    [('AWSAccessKeyId', access_key_id), 
     ('AssociateTag', 'bookpro3301-21'), 
     ('Keywords', s),
     ('Operation', 'ItemSearch'),
     ('ResponseGroup', 'Images,ItemAttributes,Offers'),
     ('SearchIndex', 'Books'),
     ('Service', 'AWSECommerceService'),
     #('Sort', 'relevancerank'),
     ('Timestamp',datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%SZ')),
    ])

   # payload = {
   #     'AWSAccessKeyId': access_key_id,
   #     'AssociateTag': 'bookpro3301-21',
   #     'Keywords': s,
   #     'Operation': 'ItemSearch',
   #     'ResponseGroup': 'Images,ItemAttributes,Offers',
   #     'SearchIndex': 'Books',
   #     'Service': 'AWSECommerceService',
   #     #'Sort': 'relevancerank',
   #     'Timestamp': '2017-12-27T02:20:19Z'#datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%SZ'),
   # }
    canonical_querystring = urllib.parse.urlencode(payload).replace('+', '%20')
    string_to_sign = "GET\n" + endpoint + "\n" + uri + "\n" + canonical_querystring
#    print (string_to_sign)
    dig = hmac.new( bytes(secret_key,'ascii'), msg=bytes(string_to_sign, 'ascii'), digestmod=sha256)
    sig = base64.b64encode(dig.digest())
#    print (sig)
    payload['Signature'] = sig
    r = requests.get("http://" + endpoint + uri, params=payload)
    #print (r.text)
    data = xmltodict.parse(r.text)['ItemSearchResponse']['Items']['Item']
    if len(data) > 0:
        pass
    else:
        return -1
#    print(json.dumps(xmltodict.parse(r.text), indent=4))
    comp = {
        'title': data[0]['ItemAttributes']['Title'],
        'author': data[0]['ItemAttributes']['Author'],
        'offer_link': data[0]['Offers']['MoreOffersUrl'],
        'link': data[0]['DetailPageURL'],
        'image': data[0]['LargeImage']['URL'],
        'price': float(data[0]['OfferSummary']['LowestNewPrice']['FormattedPrice'][4:].replace(',','')),
        'ISBN': data[0]['ItemAttributes']['ISBN'],
        'provider': 'https://images-na.ssl-images-amazon.com/images/G/01/SellerCentral/legal/amazon-logo_transparent.png'
    }
    return comp

if __name__ == "__main__":
	amazon("masala")
