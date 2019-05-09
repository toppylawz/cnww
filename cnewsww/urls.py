from django.urls import path, include
from django.urls import path
from .import views

app_name='cryptos'
urlpatterns = [
    path('', views.home, name='home'),
    path('single/', views.data, name='single')
]