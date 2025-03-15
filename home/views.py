from django.shortcuts import render,redirect
from .models import MenuItem
from .forms import QueryForm
# Create your views here.
def home_page(request):
    logged_customer = LoggedInCustomer.objects.first()
    print(f"DEBUG: Logged In Customer: {logged_customer}")
    return render(request,'home/index.html',{'logged_customer':logged_customer})

def about(request):
    return render(request,'home/about.html')


from django.shortcuts import render
from .models import MenuItem, CartItem, LoggedInCustomer


def menu_view(request):
    menu_items = MenuItem.objects.all()

    # Check if a user is logged in
    logged_in_user = LoggedInCustomer.objects.first()  # Adjust this logic if needed
    cart_count = 0

    if logged_in_user:
        cart_count = CartItem.objects.filter(customer=logged_in_user.customer).count()

    return render(request, "home/menu.html", {"menu_items": menu_items, "cart_count": cart_count})


def contact(request):
    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')  # Redirect to the same page after submission
    else:
        form = QueryForm()

    return render(request, 'home/contact.html', {'form': form})

from django.contrib import messages

from .models import Customer,LoggedInCustomer
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer, LoggedInCustomer

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer, LoggedInCustomer

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer, LoggedInCustomer  # Ensure models are imported


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")  # Ensure 'username' matches the form field name
        password = request.POST.get("password")

        try:
            customer = Customer.objects.get(name=username, password=password)  # Validate credentials

            # Update or create a logged-in customer record
            logged_customer, created = LoggedInCustomer.objects.update_or_create(
                customer=customer,
                defaults={"name": customer.name, "email": customer.email, "mobile": customer.mobile}
            )

            print(f"Logged in: {logged_customer.name}, {logged_customer.email}, {logged_customer.mobile}")  # Debugging

            return redirect("home")  # Redirect after login
        except Customer.DoesNotExist:
            messages.error(request, "Invalid username or password.")

    return render(request, "home/login.html")


def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        mobile = request.POST["mobile"]
        password = request.POST["password"]

        # Check if the username already exists
        if Customer.objects.filter(name=name).exists():
            messages.error(request, "Username already exists. Please choose another.")
            return redirect("login")

        # Check if the email is already registered
        if Customer.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered. Please use another email.")
            return redirect("login")

        # Check if the mobile number is already registered
        if Customer.objects.filter(mobile=mobile).exists():
            messages.error(request, "Mobile number is already registered. Please use another number.")
            return redirect("login")

        # Create and save the new customer
        customer = Customer(name=name, email=email, mobile=mobile, password=password)
        customer.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect("login")

    return render(request, "home/login.html")

from django.contrib.auth import logout


def logout_view(request):
    LoggedInCustomer.objects.all().delete()  # Clears all logged-in customers
    return redirect("login")  # Redirects to login page


from django.shortcuts import render
from .models import LoggedInCustomer

from django.shortcuts import render
from .models import LoggedInCustomer, OrderItem


def profile_view(request):
    logged_customer = LoggedInCustomer.objects.first()  # Get the first logged-in customer

    orders = OrderItem.objects.filter(customer=logged_customer.customer).order_by(
        '-order_date') if logged_customer else []

    return render(request, 'home/profile.html', {
        'logged_customer': logged_customer,
        'orders': orders
    })


from django.http import JsonResponse
from .models import CartItem, MenuItem, LoggedInCustomer

from django.http import JsonResponse
from .models import MenuItem, CartItem, Customer, LoggedInCustomer


def add_to_cart(request):
    if request.method == "POST":
        menu_item_id = request.POST.get("menu_id")

        # Check if menu_id is provided
        if not menu_item_id:
            return JsonResponse({"status": "error", "message": "Invalid menu item ID"}, status=400)

        try:
            # Convert to integer and fetch the MenuItem
            menu_item = MenuItem.objects.get(id=int(menu_item_id))
        except (ValueError, MenuItem.DoesNotExist):
            return JsonResponse({"status": "error", "message": "Menu item does not exist"}, status=404)

        # Fetch the logged-in customer
        try:
            logged_in_customer = LoggedInCustomer.objects.first()  # Adjust based on your login logic
            customer = logged_in_customer.customer
        except AttributeError:
            return JsonResponse({"status": "error", "message": "No logged-in customer"}, status=403)

        # Check if item already exists in the cart
        cart_item, created = CartItem.objects.get_or_create(customer=customer, menu_item=menu_item)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        # Count items in the cart
        cart_count = CartItem.objects.filter(customer=customer).count()

        return JsonResponse({"status": "success", "message": "Item added to cart", "cart_count": cart_count})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


def menu(request):
    logged_in_customer = LoggedInCustomer.objects.first()
    cart_count = 0
    if logged_in_customer:
        cart_count = CartItem.objects.filter(customer=logged_in_customer.customer).count()

    menu_items = MenuItem.objects.all()
    return render(request, "menu.html", {"menu_items": menu_items, "cart_count": cart_count})

from django.http import JsonResponse
from .models import CartItem, LoggedInCustomer

def cart_items(request):
    logged_in_customer = LoggedInCustomer.objects.first()
    if not logged_in_customer:
        return JsonResponse({"cart_items": []})

    cart_items = CartItem.objects.filter(customer=logged_in_customer.customer)
    data = {
        "cart_items": [
            {
                "menu_item_name": item.menu_item.name,
                "quantity": item.quantity,
                "total_price": item.quantity * item.menu_item.price,
            }
            for item in cart_items
        ]
    }
    return JsonResponse(data)


from django.shortcuts import render
from .models import CartItem, LoggedInCustomer

from django.shortcuts import render, redirect
from .models import CartItem, LoggedInCustomer


def cart_view(request):
    logged_in_customer = LoggedInCustomer.objects.first()
    if not logged_in_customer:
        return render(request, "home/cart.html",
                      {"cart_items": [], "total_price": 0, "error": "No logged-in user found."})

    cart_items = CartItem.objects.filter(customer=logged_in_customer.customer)

    # Compute total price per item
    for item in cart_items:
        item.total_price = item.quantity * item.menu_item.price  # Add a new attribute

    total_price = sum(item.total_price for item in cart_items)

    return render(request, "home/cart.html", {"cart_items": cart_items, "total_price": total_price})


from django.http import JsonResponse
from .models import CartItem, LoggedInCustomer

def clear_cart(request):
    if request.method == "POST":
        logged_in_customer = LoggedInCustomer.objects.first()  # Get the logged-in user
        if logged_in_customer:
            CartItem.objects.filter(customer=logged_in_customer.customer).delete()
            return JsonResponse({"success": True, "message": "Cart cleared successfully!"})
        else:
            return JsonResponse({"success": False, "message": "No user logged in!"})
    return JsonResponse({"success": False, "message": "Invalid request!"})



from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import LoggedInCustomer, MenuItem, CartItem, OrderItem

def checkout(request):
    try:
        logged_in_customer = LoggedInCustomer.objects.first()  # Get the logged-in customer
        customer = logged_in_customer.customer  # Extract actual Customer instance
    except (LoggedInCustomer.DoesNotExist, AttributeError):
        return redirect('login')

    cart_items = CartItem.objects.filter(customer=customer)

    if not cart_items.exists():
        return redirect('menu')

    total_price = sum(item.menu_item.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        # Store order details in OrderItem model
        for cart_item in cart_items:
            OrderItem.objects.create(
                customer=customer,
                menu_item=cart_item.menu_item,
                quantity=cart_item.quantity,
                total_price=cart_item.menu_item.price * cart_item.quantity,
            )

        # Clear cart after order placement
        cart_items.delete()

        return JsonResponse({'success': True, 'message': 'Order placed successfully!'})

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})
