from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name = 'signup'),
    
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('category/<int:category_id>/', views.category_view, name='category_view'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('login/google/', views.google_login_view, name='google_login'),
]
