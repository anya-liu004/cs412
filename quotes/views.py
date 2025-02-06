from django.shortcuts import render
from django.http import HttpResponse
import time
import random

# Global lists of quotes and images
QUOTES = [
    "Be at war with your vices, at peace with your neighbors, and let every new year find you a better man.",
    "Never leave that till tomorrow which you can do today.",
    "Every man…is, of common right, and by the laws of God, a freeman, and entitled to the free enjoyment of liberty."
]

IMAGES = [
    "https://hips.hearstapps.com/hmg-prod/images/benjamin-franklin_editedjpg.jpg?crop=1.00xw:1.00xh;0,0&resize=1200:*",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS0Bj7sdyj8sKLwOYaTMfc1NdO8BTun_sm2dA&s",
    "https://assets.editorial.aetnd.com/uploads/2009/11/benjamin-franklin-credit-fineart-alamy-stock.jpg"
]

# Quote view
def quote(request):
    """
    Define a view to show the 'quote.html' template.
    This view selects one random quote and one random image.
    """
    template = 'quotes/quote.html'

    # Select a random quote and image
    random_quote = random.choice(QUOTES)
    random_image = random.choice(IMAGES)

    # Context for the template
    context = {
        'quote': random_quote,
        'image_url': random_image
    }

    return render(request, template, context)

# About view
def about(request):
    """
    Define a view to show the 'about.html' template.
    """
    template = 'quotes/about.html'

    return render(request, template)

# Show all quotes and images view
def show_all(request):
    """
    Define a view to show all quotes and images in the 'show_all.html' template.
    """
    template = 'quotes/show_all.html'

    # Context for the template
    context = {
        'quotes': QUOTES,
        'images': IMAGES
    }

    return render(request, template, context)
