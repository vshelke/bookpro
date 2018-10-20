import time
from django.shortcuts import render
from find_books.integrations.amazon import Amazon
from find_books.integrations.flipkart import Flipkart
from find_books.integrations.infibeam import Infibeam


def validate_price(items=None):
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
    start = time.time()
    q = request.GET.get('q')
    threads = [Amazon(q), Flipkart(q), Infibeam(q)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    all_items = []
    relevant = []
    for thread in threads:
        if validate_price(thread.items):
            all_items.extend(thread.items)
            relevant.extend(thread.items[:2])
    all_items = sort_price(all_items)
    relevant = sort_price(relevant)
    print (q + " = " + str(time.time() - start))
    return render(request, 'find_books/results.html', {'all': all_items, 'relevant': relevant, 'query': q})
