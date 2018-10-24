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
    threads = [Amazon(query), Flipkart(query), Infibeam(query), BooksMela(query)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    all_items = []
    relevant = []
    for thread in threads:
        items = validate_price(thread.items)
        if items:
            all_items.extend(items)
            relevant.extend(items[:2])
    all_items = sorted(all_items, key=lambda k: k['price'])
    relevant = sorted(relevant, key=lambda k: k['price'])
    all_items = [x for x in all_items if x not in relevant]
    _LOGGER.debug("Query: (" + query + ") took (" + str(time.time() - start) + ") secs")
    
    return render(request, 'find_books/results.html', {'all': all_items, 'relevant': relevant, 'query': query})
