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
            'provider': 'https://www.findshopindia.com/uploads/assets/logo/250x150/20171218080244.png'
        }
        title = self.check(product.find("div", {"class": "product-info"}))
        if title:
            
            if title.find("span", {"class": "abc-author"}): 
                data['author'] = self.check(title.find("span", {"class": "abc-author"}).get_text()[4:])

            if title.find("h2", {"class": "product-name"}).find("a")['href']:
                data['link'] = self.check(title.find("h2", {"class": "product-name"}).find("a")['href'])
            
            if title.find("h2", {"class": "product-name"}).find("a")['href'][-13:]:
                data['ISBN'] = self.check(title.find("h2", {"class": "product-name"}).find("a")['href'][-13:])
            
            if title.find("div", {"class": "price-box"}).find("p", {"class":"special-price"}).find("span", {"class":"price"}).get_text().strip()[1:].replace(',',''):
                data['price'] = float(self.check(title.find("div", {"class": "price-box"}).find("p", {"class":"special-price"}).find("span", {"class":"price"}).get_text().strip()[1:].replace(',','')))

            if product.find('img')['src']:
                data['image'] = self.check(product.find('img')['src'])
            
            if title.find("h2",{"class":"product-name"}).find('a').get_text():
                data['title'] = self.check(title.find("h2",{"class":"product-name"}).find('a').get_text())
            
        return data

    def run(self):
        url = 'https://www.booksmela.com/catalogsearch/result/?q= ' + self.query
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        products = soup.findAll("li",{"class": "item last"})
        if len(products) <= 0:
            return None
        for product in products:
            self.items.append(self.parse_product(product))
