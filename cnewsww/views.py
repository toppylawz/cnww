from django.shortcuts import render,redirect
from django.contrib import messages
from urllib import request
import requests
import json

def home(request):

    # this fetch the crypto table
    data_request =requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,DASH,ZEC,ETH,LTC,DOGE,BAT,XMR,BCH,NEO,ADA,XRP&tsyms=USD")
    table_data = json.loads(data_request.content)
    # this fetch the news update
    api_request =requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
    api_content = json.loads(api_request.content)
    collector={
        'api': api_content, 'data': table_data
        }
    return render(request, 'cnewsww/home.html', collector)
