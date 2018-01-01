from hashlib import sha256
from bs4 import BeautifulSoup
import time, datetime, base64, hmac, requests, urllib, xmltodict, json


def check(element):
  return '' if element is None else element

def infibeam(s):
    url = 'https://www.infibeam.com/search?q=' + s + '&us=true&sort=relevance'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    i = soup.findAll("div", { "class" : " col-md-3 col-sm-6 col-xs-12 search-icon flex-item" })
    # with open('infibeam_data.json', 'w') as f:
    #     json.dump(str(i), f, indent=4)
    if len(i) <= 0:
        return None
    comp = []
    for product in i:
        title = ''
        author = ''
        ISBN = ''
        offer_link = ''
        image = ''
        price = None
        link = ''
        title = check(product.find("div", { "class" : "title" }))
        if title:
            if check(title.find("div", { "class" : "author" })):
                author = title.find("div", { "class" : "author" }).get_text()
            link = "https://www.infibeam.com" + title.a['href'] + "&trackId=bookpro3301"
        if check(product.find("span", { "class" : "discount" })):
            ISBN = product.find("span", { "class" : "discount" }).get_text()
        if check(product.find("span", { "class" : "final-price" })):
            price = product.find("span", { "class" : "final-price" }).get_text()
            try:
                price = float(price[4:].replace(',',''))
            except:
                price = None
        comp.append({
            'title': check(title.a.string),
            'author': author,
            'offer_link': '',
            'link': link,
            'image': check(product.source['srcset']),
            'price': price,
            'ISBN': ISBN,
            'provider': 'https://assets.infibeam.net/assets/skins/common/images/infibeam_logo.png?v=2'
        })
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
