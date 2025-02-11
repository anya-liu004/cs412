from django.shortcuts import render
from django.http import HttpResponse
import random
import datetime

# Prices for menu items
MENU_PRICES = {
    "Cookies": 2.00,
    "Brownie": 3.00,
    "Muffin": 4.00,
}

# Dictionary of specials with prices
SPECIALS = {
    "Berry Bliss Tart": 4.50,
    "Lemon Passionfruit Tart": 5.00,
    "Cozy Cinnamon Roll": 3.75,
    "Caramel Crunch Croissant": 4.25,
    "Maple Glaze Donut": 3.50,
    "Matcha Muffins": 4.00,
    "Pumpkin Spice Scones": 3.75,
    "Coconut Cream Puffs": 4.75,
}

# Main view
def main(request):
    """
    Define a view to show the 'main.html' template for the main page. 
    """
    template = 'restaurant/main.html'
    return render(request, template)

# Order view
def order(request):
    """
    Show the web page with the form.
    """
    template = 'restaurant/order.html'

    # Select a random special from the dictionary
    random_special, special_price = random.choice(list(SPECIALS.items()))

    # Context for the template
    context = {
        'special': random_special,
        'special_price': special_price
    }

    return render(request, template, context)

# Confirmation view for submitting form
# def confirmation(request):
#     """
#     Define a view to the 'confirmation.html' template. 
#     """
#     template = 'restaurant/confirmation.html'

#     # Read the form data into Python variables:
#     if request.POST:
#         name = request.POST['name']
#         favorite_color = request.POST['favorite_color']

#         context = {
#             'name': name,
#             'favorite_color': favorite_color,
#         }

#     return render(request, template, context)

def confirmation(request):
    """
    Process the order form submission and display the confirmation page.
    """
    template = 'restaurant/confirmation.html'

    if request.method == "POST":
        # Retrieve customer details
        name = request.POST.get('name', 'N/A')
        phone = request.POST.get('phone', 'N/A')
        email = request.POST.get('email', 'N/A')

        # Retrieve selected menu items
        selected_items = request.POST.getlist('items')  # Gets all selected checkboxes
        toasted_option = request.POST.get('toasted?', 'None')
        special_instructions = request.POST.get('instructions', '')

        # Calculate total price
        total_price = 0.0
        ordered_items = []

        for item in selected_items:
            if item == "daily_special":  
                # Retrieve the special chosen in the order page
                special_name = request.session.get('special', 'Daily Special')
                special_price = request.session.get('special_price', 5.00)
                ordered_items.append(f"{special_name} - ${special_price:.2f}")
                total_price += special_price
            else:
                price = MENU_PRICES.get(item, 0.00)
                ordered_items.append(f"{item} - ${price:.2f}")
                total_price += price

        # Generate a random ready time (30-60 minutes from now)
        ready_time = datetime.datetime.now() + datetime.timedelta(minutes=random.randint(30, 60))

        # Context to pass to the template
        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'ordered_items': ordered_items,
            'toasted_option': toasted_option,
            'special_instructions': special_instructions,
            'total_price': f"{total_price:.2f}",  # Format to 2 decimal places
            'ready_time': ready_time.strftime("%I:%M %p")  # Format as HH:MM AM/PM
        }

        return render(request, template, context)

    # If accessed without POST request, redirect to order page
    return render(request, 'restaurant/order.html')
