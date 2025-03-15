from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='food_images/')  # Store image filename (e.g., "pizza.jpg")

    def __str__(self):
        return self.name


class Queries(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


from django.db import models
class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name will act as username
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=100)



    def __str__(self):
        return self.name

class LoggedInCustomer(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,default='')
    email = models.EmailField(default='')
    mobile = models.CharField(max_length=15,default=0)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.customer.name} - {self.menu_item.name} ({self.quantity})"

class OrderItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.menu_item.name} ({self.quantity})"
