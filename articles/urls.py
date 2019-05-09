from django.urls import path
from django.conf.urls import url
from .views import (
    articles, article_details,create_article, delete_article,articles_update
)


app_name='articles'

urlpatterns = [
    path('', articles, name="list"),
    url(r'^create_article/$',create_article, name="create_article"),
    url(r'^(?P<slug>[\w-]+)/delete/$', delete_article),
    url(r'^(?P<slug>[\w-]+)/edit/$', articles_update, name='edit'),
    url(r'^(?P<slug>[\w-]+)/$', article_details, name="detail"),
]
