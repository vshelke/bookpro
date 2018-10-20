from django.conf.urls import url
from find_books import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/', views.query, name='query'),
]
