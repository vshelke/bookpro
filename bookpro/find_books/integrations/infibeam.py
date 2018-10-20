import time, datetime, base64, hmac, requests, urllib, xmltodict, json
from bs4 import BeautifulSoup
from hashlib import sha256
from threading import Thread


class Infibeam(Thread):
    def __init__(self, query):
        super(Infibeam, self).__init__()
        self.query = query
        self.items = []

    def check(self, element):
        return '' if element is None else element

    def run(self):
        url = 'https://www.infibeam.com/search?q=' + self.query + ' book&us=true&sort=relevance'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        products = soup.findAll("div", { "class" : " col-md-3 col-sm-6 col-xs-12 search-icon flex-item" })
        if len(products) <= 0:
            return None
        for product in products:
            title = ''
            author = ''
            ISBN = ''
            offer_link = ''
            image = ''
            price = None
            link = ''
            title = self.check(product.find("div", { "class" : "title" }))
            if title:
                if self.check(title.find("div", { "class" : "author" })):
                    author = title.find("div", { "class" : "author" }).get_text()
                link = "https://www.infibeam.com" + title.a['href'] + "&trackId=bookpro3301"
            if self.check(product.find("span", { "class" : "discount" })):
                ISBN = product.find("span", { "class" : "discount" }).get_text()
            if self.check(product.find("span", { "class" : "final-price" })):
                price = product.find("span", { "class" : "final-price" }).get_text()
                try:
                    price = float(price[4:].replace(',',''))
                except:
                    price = None
            self.items.append({
                'title': self.check(title.a.string),
                'author': author,
                'offer_link': '',
                'link': link,
                'image': self.check(product.source['srcset']),
                'price': price,
                'ISBN': ISBN,
                'provider': 'https://assets.infibeam.net/assets/skins/common/images/infibeam_logo.png?v=2'
            })
