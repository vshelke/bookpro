import time
import json
import logging
from django.shortcuts import render
from find_books.integrations import Amazon, Flipkart, Infibeam, BooksMela

_LOGGER = logging.getLogger(__name__)


def validate_price(items=[]):
    """ This function checks a list of items and returns a validated list with items who have float price only.

    Args:
        items (list): a list of dictionaries.

    Returns:
        list: returns a list of dictionaries with float not none price key.

    """
    
    validated = []
    for item in items:
        if not item['price'] == None and isinstance(item['price'], float):
            validated.append(item)
    return validated


def filter_price(items, min_price=0, max_price=5000000):
    filtered = []
    for item in items:
        if min_price <= item['price'] and item['price'] <= max_price:
            filtered.append(item)
    return filtered


def index(request):
    """View function for the home page of site.

    Args:
        request: the request we recive from the user.

    Returns:
        A render object that was rendered with 'find_books/index.html' template

    """
    
    #Renders the HTML template find_books/index.html.
    return render(request, 'find_books/index.html')


def search(request):
    """View function for the results.html page.

    Args:
        request: the request we recive from the user.

    Returns:
        A render object that was rendered with 'find_books/results.html' template and context.

    """
    
    start = time.time()
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        min_price = float(min_price)
    else:
        min_price = 0

    if max_price:
        max_price = float(max_price)
    else:
        max_price = 100000

    threads = [Amazon(query), Flipkart(query), Infibeam(query), BooksMela(query)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    all_items = []
    relevant = []
    for thread in threads:
        items = filter_price(validate_price(thread.items), min_price, max_price)
        if items:
            all_items.extend(items)
            relevant.extend(items[:2])

    all_items = sorted(all_items, key=lambda k: k['price'])
    relevant = sorted(relevant, key=lambda k: k['price'])
    _LOGGER.debug("Query: (" + query + ") took (" + str(time.time() - start) + ") secs")
    return render(request, 'find_books/results.html', {'all': all_items, 'relevant': relevant, 'query': query, 'min_price': min_price, 'max_price': max_price})

