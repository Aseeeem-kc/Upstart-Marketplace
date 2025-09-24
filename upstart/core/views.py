from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from item.models import Category, Item
from .forms import CustomUserCreationForm
from .models import CustomUser
import uuid
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import os

import requests
from django.conf import settings  # optional for dynamic host config

def index(request):
    user = request.user
    items = Item.objects.filter(is_sold=False)[:8]
    categories = Category.objects.all()

    recommendations = []

    if user.is_authenticated:
        try:
            # You can store the FastAPI URL in settings.py as FASTAPI_RECOMMENDER_URL
            response = requests.get(
                f"http://localhost:8001/recommendations/",
                params={'user_id': user.id, 'limit': 5}
            )
            response.raise_for_status()
            recommended_ids = response.json().get("recommended_items", [])
            recommendations = Item.objects.filter(id__in=recommended_ids, is_sold=False)
        except requests.RequestException as e:
            print(f"Error fetching recommendations: {e}")
            recommendations = []

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
        'user': user,
        'recommendations': recommendations
    })  

# def index(request):

#     user = request.user
#     print(user)
#     items = Item.objects.filter(is_sold=False)[0:6]
#     categories = Category.objects.all()
#     return render(request, 'core/index.html', {
#         'categories': categories,
#         'items': items,
#         'user':user
#     })

def verify_email(request, token):
    try:
        user = CustomUser.objects.get(email_token=token)
        user.is_active = True
        user.is_verified = True
        user.email_token = '' 
        user.save()
        messages.success(request, 'Your email has been verified.')
    except CustomUser.DoesNotExist:
        messages.error(request, 'Invalid verification link.')

    return redirect('core:login')  

def contact(request):
    return render(request, 'core/contact.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.email_token = str(uuid.uuid4())
            user.save()

            # Sending the verification email
            verification_url = request.build_absolute_uri(
                reverse('core:verify_email', kwargs={'token': user.email_token})
            )
            messages.success(request, f"New account created for {user.username}. Please check your email for link to activate your account before logging in.")
            send_mail(
                'Verify your email address',
                f'Click the link to verify your email address: {verification_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                auth_password=os.getenv('EMAIL_APP_PASSWORD'),
            )

            
            return redirect('core:login')
        else:
            messages.error(request, 'There was an error with your form.')
            print('Form is not valid:', form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'core/signup.html', {
        'form': form
    })



def login(request):
   
    if request.method == 'POST':
        
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.is_active == False:
                print('Please activate your account through email before logging in')

            return redirect('core:index')
        else:
            print('Form is not valid:', form.errors)
    else:
        
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {
        'form': form,
    })

def google_login_view(request):
    return render(request, 'google_login.html')

def logout(request):
    auth_logout(request)
    return redirect('core:index')

def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    items = Item.objects.filter(category=category, is_sold=False)
    return render(request, 'core/category.html', {
        'category': category,
        'items': items,
    })


    