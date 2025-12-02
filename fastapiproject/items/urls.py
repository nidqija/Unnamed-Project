# Assuming your views.py has:
# from .views import index, custom_admin_login

from django.urls import path
from .views import index, custom_admin_login

urlpatterns = [
    # 1. Homepage: maps the root URL (e.g., http://127.0.0.1:8000/)
    path('', index, name='index'), 
    
    # 2. Login Page: maps to the custom authentication view
    # The trailing slash ('/') is the convention.
    path('login/', custom_admin_login, name='login'), 
    
    # Optional: You can remove the conflicting and incorrect login path entries.
]