from django.shortcuts import render
from find_books.api import amazon, flipkart, misc

def index(request):
    return render(request, 'find_books/index.html')

def query(request):
    q = request.GET['query']
    #
    amazon_item = amazon.amazon(q)
    flipkart_item = flipkart.flipkart(q)
    infibeam_item = misc.infibeam(q)
    sapna_item = misc.sapnaonline(q)
    #booksmela_item = booksmela(q)
    i = [ amazon_item, flipkart_item, infibeam_item, sapna_item ]
    i = sorted(i, key=lambda k: k['price'])
    return render(request, 'find_books/results.html', {'data': i, 'query': q})
