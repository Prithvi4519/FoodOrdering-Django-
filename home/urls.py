from django.urls import path


from .views import home_page, about, menu_view, contact, login_view, register, logout_view, profile_view, add_to_cart, \
    cart_items, cart_view, clear_cart, checkout

urlpatterns=[
    path('', login_view, name='login'),
    path('home/',home_page,name='home'),
    path('about/',about,name='about'),
    path('menu/',menu_view,name='menu'),
    path('contact/', contact, name='contact'),
path("login/", login_view, name="login"),
    path("register/", register, name="register"),
    path('logout/', logout_view, name='logout'),
    path('profile/',profile_view,name='profile'),
    path('add_to_cart/',add_to_cart,name='add_to_cart'),
path('cart_items/', cart_items, name='cart_items'),
path('cart/', cart_view, name='cart'),
path('cart/', cart_view, name='cart'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('checkout/', checkout, name='checkout'),
]