import random
import uuid

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, CustomUser, Product, sliderImage


def get_categories_with_products():
    return Category.objects.filter(is_active=True).prefetch_related(
        Prefetch(
            'product_set',
            queryset=Product.objects.filter(is_active=True).order_by('-created_at'),
            to_attr='active_products',
        )
    ).order_by('name')


def home(request):
    slider_images = sliderImage.objects.all().order_by('id')
    categories = get_categories_with_products()
    return render(request, 'home.html', {
        'slider_images': slider_images,
        'categories': categories,
    })


def product(request):
    categories = get_categories_with_products()
    uncategorized_products = Product.objects.filter(
        category__isnull=True,
        is_active=True,
    ).order_by('-created_at')
    return render(request, 'product.html', {
        'categories': categories,
        'uncategorized_products': uncategorized_products,
    })


def category(request):
    categories = get_categories_with_products()
    return render(request, 'category.html', {'categories': categories})


def gallery(request):
    return render(request, 'gallery.html')


def about_us(request):
    return render(request, 'about_us.html')


def wishlist(request):
    return render(request, 'wishlist.html')


def cart(request):
    cart_data = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart_data.keys(), is_active=True)
    cart_items = []
    total = 0

    for product_item in products:
        quantity = cart_data.get(str(product_item.id), 0)
        subtotal = product_item.price * quantity
        total += subtotal
        cart_items.append({
            'product': product_item,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


def add_to_cart(request, product_id):
    product_item = get_object_or_404(Product, id=product_id, is_active=True)
    cart_data = request.session.get('cart', {})
    product_key = str(product_item.id)
    cart_data[product_key] = cart_data.get(product_key, 0) + 1
    request.session['cart'] = cart_data
    request.session.modified = True
    messages.success(request, f'{product_item.name} added to cart.')
    return redirect(request.POST.get('next') or 'product')


def buy_now(request, product_id):
    product_item = get_object_or_404(Product, id=product_id, is_active=True)
    cart_data = request.session.get('cart', {})
    product_key = str(product_item.id)
    cart_data[product_key] = cart_data.get(product_key, 0) + 1
    request.session['cart'] = cart_data
    request.session.modified = True
    messages.success(request, f'{product_item.name} is ready to buy.')
    return redirect('cart')


def my_profile(request):
    return render(request, 'my_profile.html')


def my_orders(request):
    return render(request, 'my_orders.html')


def logout_view(request):
    auth_logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('home')


def send_registration_otp(email, otp):
    send_mail(
        'Verify your Flipkart Pro email',
        f'Your Flipkart Pro registration OTP is {otp}.',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )


def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        form_data = {
            'full_name': full_name,
            'email': email,
        }

        if not full_name or not email or not password or not confirm_password:
            messages.error(request, 'Please fill all fields.')
            return render(request, 'register.html', form_data)

        if password != confirm_password:
            messages.error(request, 'Password and confirm password do not match.')
            return render(request, 'register.html', form_data)

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'register.html', form_data)

        username = email.split('@')[0]

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'register.html', form_data)

        otp = str(random.randint(100000, 999999))
        request.session['pending_registration'] = {
            'full_name': full_name,
            'email': email,
            'password': password,
            'username': username,
            'mobile_no': f'u{uuid.uuid4().hex[:14]}',
            'otp': otp,
        }

        try:
            send_registration_otp(email, otp)
        except Exception as error:
            error_message = 'Could not send OTP email. Please check SMTP settings and try again.'
            if settings.DEBUG:
                error_message = f'{error_message} Error: {error}'
            messages.error(request, error_message)
            return render(request, 'register.html', form_data)

        messages.success(request, 'OTP sent to your email. Please verify to complete registration.')
        return redirect('verify_register_otp')

    return render(request, 'register.html')


def verify_register_otp(request):
    pending_registration = request.session.get('pending_registration')

    if not pending_registration:
        messages.error(request, 'Please register first.')
        return redirect('register')

    if request.method == 'POST':
        otp = request.POST.get('otp', '').strip()

        if not otp:
            messages.error(request, 'Please enter OTP.')
            return render(request, 'verify_otp.html', {'email': pending_registration['email']})

        if otp != pending_registration['otp']:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'verify_otp.html', {'email': pending_registration['email']})

        user = CustomUser.objects.create_user(
            username=pending_registration['username'],
            email=pending_registration['email'],
            password=pending_registration['password'],
            full_name=pending_registration['full_name'],
            mobile_no=pending_registration['mobile_no'],
        )
        request.session.pop('pending_registration', None)
        auth_login(request, user)

        send_mail(
            'Welcome to Flipkart Pro',
            'Your email has been verified and your Flipkart Pro registration is complete.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )

        messages.success(request, 'Registration successful.')
        return redirect('/')

    return render(request, 'verify_otp.html', {'email': pending_registration['email']})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, 'Please fill all fields.')
            return render(request, 'login.html')

        try:
            user_obj = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user_obj = None

        user = authenticate(
            request,
            username=user_obj.username if user_obj else email,
            password=password,
        )

        if user is None:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')

        auth_login(request, user)
        messages.success(request, 'Login successful.')
        return redirect('/')

    return render(request, 'login.html')
