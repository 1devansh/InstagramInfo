from django.shortcuts import render
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models

# Create your views here.
BASE_CRAIGSLIST_URL = 'https://www.instagram.com/{}'

def home(request):
  return render(request, 'base.html')


def new_search(request):
  search = request.POST.get('search')

  models.Search.objects.create(search=search)

  final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search)) 
  response = requests.get(final_url)

  data = response.text
  soup = BeautifulSoup(data, features='html.parser')

  
  
  post_listings = soup.find('meta', property="og:description")

  info = post_listings.attrs['content']
  

  info = info.split('-')[0]

  followers = info.split(',')[0].split(' ')[0]
  following = info.split(',')[1].strip().split(' ')[0]
  posts = info.split(',')[2].strip().split(' ')[0]

  

  image_source = soup.find('meta', property="og:image")
  image_source = image_source.attrs['content']
  

  final = [followers, following, posts, image_source, final_url]
  print(final)
  stuff_for_frontend={
    'search': search, 
    'final_postings': final,
  }
  return render(request, 'myapp/new_search.html', stuff_for_frontend)
