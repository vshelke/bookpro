import requests
from bs4 import BeautifulSoup
from threading import Thread
import xmltodict

class Bookswagon(Thread):
    """Class Bookswagon to scrape data from bookswagon site.

   Args:
       None

   Returns:
       None.
   """
    def __init__(self, query):
        """init function to initialize class.

       Args:
           query string to search

       Returns:
           Nothing.
       """
        super(Bookswagon, self).__init__()
        self.query = query
        self.items = []

    def check(self, element):
        """
        check function to check if value of  element exits if true return
        else return empty.

       Args:
           element to check

       Returns:
           element if exists else empty string.
       """
        return '' if element is None else element


    def parse_product(self, product):
        """
        parsing function to parse all the values needs to render on web page
        for each book.

       Args:
           each product

       Returns:
           parsed object for each product.

       """
        data = {
            'title': '',
            'author': '',
            'offer_link': '',
            'link': '',
            'image': '',
            'price': None,
            'ISBN': '',
            'provider': 'https://www.bookswagon.com/images/logos/logo-new.png'
        }

        title = product.find("div",{"class":"title"})
        author = product.find("div",{"class":"author-publisher"})
        img = product.find("img")
        book_cover=product.find("div",{"class":"cover"})
        a_tag = book_cover.find("a")
        price = product.find("div",{"class":"sell"})
        discount = product.find("span",{"class":"cover-discount-tag"})
        link = a_tag['href']

        if self.check(title):
            data['title'] = title.text
        if(self.check(author)):
            data['author'] = author.text
        if(self.check(link)):
            data['link'] = link
        if(self.check(price)):
            data['price'] = float(price.text[3:].replace(',', ''))
        if(self.check(img)):
            r = requests.head(img['src'])
            if(r.status_code != requests.codes.ok):
                data['image'] = "https://d2g9wbak88g7ch.cloudfront.net/productimages/mainimages/notavailable.gif"
            else:
                data['image'] = img['src']
        else:
            data['image'] = "https://d2g9wbak88g7ch.cloudfront.net/productimages/mainimages/notavailable.gif"

        return data

    def run(self):
        url = 'https://www.bookswagon.com/search-books/'+self.query
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        products = soup.findAll(
            "div", {"class": "list-view-books"})
        if len(products) <= 0:
            return None
        for product in products:
            self.items.append(self.parse_product(product))
