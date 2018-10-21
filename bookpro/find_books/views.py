import time
import json
import logging
from django.shortcuts import render
from find_books.integrations import Amazon, Flipkart, Infibeam

_LOGGER = logging.getLogger(__name__)


def validate_price(items=[]):
    validated = []
    for item in items:
        if not item['price'] == None and isinstance(item['price'], float):
            validated.append(item)
    return validated


def index(request):
    return render(request, 'find_books/index.html')


def search(request):
    start = time.time()
    query = request.GET.get('q')
    threads = [Amazon(query), Flipkart(query), Infibeam(query)]
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
    _LOGGER.debug("Query: (" + query + ") took (" + str(time.time() - start) + ") secs")
    return render(request, 'find_books/results.html', {'all': all_items, 'relevant': relevant, 'query': query})
