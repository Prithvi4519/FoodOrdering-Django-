from django.contrib import admin
from .models import MenuItem, Queries, Customer, LoggedInCustomer, CartItem, OrderItem  # Import the model

# Register the model so it appears in admin
admin.site.register(MenuItem)

admin.site.register(Queries)
admin.site.register(Customer)
admin.site.register(LoggedInCustomer)
admin.site.register(CartItem)
admin.site.register(OrderItem)