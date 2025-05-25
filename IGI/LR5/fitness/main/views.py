from django.shortcuts import render
from .models import Article
import requests

def get_random_quote():
    try:
        response = requests.get('https://zenquotes.io/api/random')
        if response.status_code == 200:
            data = response.json()[0]
            return {"quote": data['q'], "author": data['a']}
    except:
        return {"quote": "Мудрость приходит со временем", "author": "Народная мудрость"}

def get_daily_advice():
    try:
        response = requests.get('https://api.adviceslip.com/advice')
        if response.status_code == 200:
            return response.json()['slip']['advice']
    except:
        return "Никогда не сдавайся!"

def home(request):
    latest_article = Article.objects.first()  # Get latest article
    quote_data = get_random_quote()
    advice = get_daily_advice()
    
    context = {
        'article': latest_article,
        'quote': quote_data['quote'],
        'philosopher': quote_data['author'],
        'advice': advice,
    }
    
    return render(request, 'main/home.html', context)
