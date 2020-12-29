from django.shortcuts import render
import requests

from . import models

from urllib.parse import quote_plus
from bs4 import BeautifulSoup

# Create your views here.
def home(request):
    return render(request, 'base.html')

BASE_URL = 'https://mumbai.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'



def newSearch(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    FINAL_URL = BASE_URL.format(quote_plus(search))
    response = requests.get(FINAL_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    post_listing = soup.find_all('li',class_='result-row')

    print(post_listing)

    final_title = []
    for post in post_listing:
        post_title = post.find(class_="result-title hdrlnk").text
        post_link = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image gallery'):
            img=post.find(class_='result-image gallery').get('data-ids').split(',')[0].split(':')[1]
            post_image_link = BASE_IMAGE_URL.format(img)

        else:
            post_image_link = 'https://craigslist.org/images/peace.jpg'

        final_title.append((post_title,post_link,post_price,post_image_link))





    context ={
        'search' :search,
        'final_title':final_title,

    }
    return render(request, 'new_search.html', context)