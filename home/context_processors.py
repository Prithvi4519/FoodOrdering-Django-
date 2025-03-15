from .models import LoggedInCustomer

def logged_customer_context(request):
    return {
        "logged_customer": LoggedInCustomer.objects.first()  # Fetch logged-in customer globally
    }
