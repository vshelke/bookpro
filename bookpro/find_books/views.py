from django.shortcuts import render
from find_books.api import amazon, flipkart, misc

def validate_price(items):
    if items:
        for item in items:
            if item['price']:
                continue
            else:
                items.remove(item)
    return items

def sort_price(items):
    return sorted(items, key=lambda k: k['price'])

def index(request):
    return render(request, 'find_books/index.html')

def query(request):
    q = request.GET['q']
    amazon_item = amazon.amazon(q)
    flipkart_item = flipkart.flipkart(q)
    infibeam_item = misc.infibeam(q)
    # sapna_item = misc.sapnaonline(q)
    # #booksmela_item = booksmela(q)
    all_items = []
    relevant = []
    if validate_price(amazon_item):
        all_items += amazon_item
        relevant += amazon_item[:2]

    if validate_price(flipkart_item):
        all_items += flipkart_item
        relevant += flipkart_item[:2]

    if validate_price(infibeam_item):
        all_items += infibeam_item
        relevant += infibeam_item[:2]

    all_items = sort_price(all_items)
    relevant = sort_price(relevant)

    return render(request, 'find_books/results.html', {'all': all_items, 'relevant': relevant, 'query': q})
