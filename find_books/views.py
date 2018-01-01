from django.shortcuts import render
from find_books.api import amazon, flipkart, misc

def validate_price(item):
    if item and item[0]['price']:
        return item
    return None


def index(request):
    return render(request, 'find_books/index.html')

def query(request):
    q = request.GET['query']
    amazon_item = amazon.amazon(q)
    flipkart_item = flipkart.flipkart(q)
    infibeam_item = misc.infibeam(q)
    # sapna_item = misc.sapnaonline(q)
    # #booksmela_item = booksmela(q)
    i = []
    if validate_price(amazon_item):
        i.append(amazon_item[0])
    if validate_price(flipkart_item):
        i.append(flipkart_item[0])
    if validate_price(infibeam_item):
        i.append(infibeam_item[0])
    i = sorted(i, key=lambda k: k['price'])
    return render(request, 'find_books/results.html', {'data': i, 'query': q})
