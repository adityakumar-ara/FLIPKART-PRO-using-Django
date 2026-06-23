from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('product/', views.product, name='product'),
    path('category/', views.category, name='category'),
    path('gallery/', views.gallery, name='gallery'),
    path('about-us/', views.about_us, name='about_us'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('register/verify-otp/', views.verify_register_otp, name='verify_register_otp'),
    path('login/', views.login_view, name='login'),
]
