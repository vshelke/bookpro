from django.shortcuts import render
from hashlib import sha256
from bs4 import BeautifulSoup
import time, datetime, base64, hmac, requests, urllib, xmltodict, json

"""
Amazon.in (done)
Flipkart.com (done)
Infibeam.com (done)

--non aff---

Snapdeal.com
Rediff.com
Sapnaonline.com (done) aff
Booksmela.com (done) aff
Buybooksindia.com (tuff)
"""

#product name, link, image, price, ISBN, provider
def amazon(s):
    access_key_id = 'AKIAJKBJSCFX6V2ODHAA'
    secret_key = "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"
    endpoint = "webservices.amazon.in"
    uri = "/onca/xml"
    payload = {
        'AWSAccessKeyId': access_key_id,
        'AssociateTag': 'bookpro3301-21',
        'Keywords': s,
        'Operation': 'ItemSearch',
        'ResponseGroup': 'Images,ItemAttributes,Offers',
        'SearchIndex': 'Books',
        'Service': 'AWSECommerceService',
        #'Sort': 'relevancerank',
        'Timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%SZ'),
    }
    canonical_querystring = urllib.parse.urlencode(payload).replace('+', '%20')
    string_to_sign = "GET\n" + endpoint + "\n" + uri + "\n" + canonical_querystring
    dig = hmac.new( bytes(secret_key,'ascii'), msg=bytes(string_to_sign, 'ascii'), digestmod=sha256)
    sig = base64.b64encode(dig.digest())
    payload['Signature'] = sig
    r = requests.get("http://" + endpoint + uri, params=payload)
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

def flipkart(s):
    token = '04f324321327484e85658ec6c396993b'
    aff_id = 'bookpro3301'
    headers = {
        'Fk-Affiliate-Id': aff_id,
        'Fk-Affiliate-Token': token,
    }
    params = {
        'query': s,
        'resultCount': 10,
    }
    endpoint = 'https://affiliate-api.flipkart.net/affiliate/1.0/search.json'
    r = requests.get(endpoint, params=params, headers=headers)
    data = json.loads(r.text)['productInfoList']
    if len(data) > 0:
        pass
    else:
        return -1
    data = data[0]
    comp = {
        'title': data['productBaseInfoV1']['title'],
        'author': data['categorySpecificInfoV1']['booksInfo']['authors'],
        'offer_link': '',#data['productBaseInfoV1']['offers'],
        'link': data['productBaseInfoV1']['productUrl'],
        'image': data['productBaseInfoV1']['imageUrls']['400x400'],
        'price': float(data['productBaseInfoV1']['flipkartSpecialPrice']['amount']),
        'ISBN': data['categorySpecificInfoV1']['keySpecs'],
        'provider': 'https://www.underconsideration.com/brandnew/archives/flipkart_logo_detail.jpg'
    }
    return comp

def check(element):
  return '' if element is None else element

def infibeam(s):
    url = 'https://www.infibeam.com/search?q=' + s
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    i = soup.findAll("div", { "class" : " col-md-3 col-sm-6 col-xs-12 search-icon flex-item" })
    if len(i) > 0:
        pass
    else:
        return -1
    data = i[0]
    try:
        author = check(data.find("div", { "class" : "title" }).find("div", { "class" : "author" }).get_text())
    except:
        author = ''
    comp = {
        'title': check(data.find("div", { "class" : "title" }).a.string),
        'author': author,
        'offer_link': '',
        'link': check("https://www.infibeam.com" + data.find("div", { "class" : "title" }).a['href'] + "&trackId=bookpro3301"),
        'image': check(data.source['srcset']),
        'price': check(float(data.find("span", { "class" : "final-price" }).get_text()[4:].replace(',',''))),
        'ISBN': '',
        'provider': 'https://assets.infibeam.net/assets/skins/common/images/infibeam_logo.png?v=2'
    }
    #append ?trackId=bookpro3301
    return comp

def sapnaonline(s):
    url = 'https://www.sapnaonline.com/general-search?searchkey=' + s
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    i = soup.findAll("li", { "class" : "large-12 twelve small-12 columns product-book-list-view" })
    if len(i) > 0:
        pass
    else:
        return -1
    data = i[0]
    try:
        image = check(data.find("img", {"class": "sapna-product-book-list-view"})['src'])
    except:
        image = ''
    comp = {
        'title': check(data.find("div", {"class": "large-12 twelve small-12 tablet-8 columns product-book-name"}).get_text().strip()),
        'author': check(data.find("div", {"class": "large-12 twelve small-12 tablet-8 columns product-book-author"}).get_text().strip()),
        'offer_link': '',
        'link': check(data.find("div", {"class": "large-12 twelve small-12 tablet-8 columns product-book-name"}).h2.a['href']),
        'image': image,
        'price': check(float(data.find("span", { "class" : "actual-price" }).get_text()[1:].strip())),
        'ISBN': check(data.find("ul", {"class": "large-12 twelve hide-for-small small-12 tablet-8 columns product-book-details-text product-book-details-specs"}).li.get_text()[6:].strip()),
        'provider': 'https://rescdn.sapnaonline.com/common/sapna/images/common_images/logo.png'
    }
    return comp

# def booksmela(s):
#     url = 'https://www.booksmela.com/catalogsearch/result/?q=' + s
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, 'html.parser')
#     i = soup.findAll("li", { "class" : "item last" })
#     data = i[0]
#     comp = {
#         'title': data.find("h2", {"class": "product-name"}).a.get_text(),
#         'author': data.find("span", {"class": "abc-author"}).get_text(),
#         'offer_link': data.find("p", {"class": "special-price yousave"}).get_text().strip(),
#         'link': data.find("h2", {"class": "product-name"}).a['href'],
#         'image': data.find("a", {"class": "product-image"}).img['src'],
#         'price': float(data.find("p", {"class": "special-price"}).find("span", {"class": "price"}).get_text().strip()),
#         'ISBN': '',
#         'provider': 'BooksMela'
#     }
#     return comp


def index(request):
    return render(request, 'find_books/index.html')

def query(request):
    q = request.GET['query']
    amazon_item = amazon(q)
    flipkart_item = flipkart(q)
    infibeam_item = infibeam(q)
    sapna_item = sapnaonline(q)
    #booksmela_item = booksmela(q)
    i = [ amazon_item, flipkart_item, infibeam_item, sapna_item ]
    i = sorted(i, key=lambda k: k['price'])
    return render(request, 'find_books/results.html', {'data': i, 'query': q})
