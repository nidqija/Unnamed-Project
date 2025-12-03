# Assuming your views.py has:
# from .views import index, custom_admin_login

from django.urls import path
from .views import index, custom_admin_login , admin_dashboard

urlpatterns = [
    # 1. Homepage: maps the root URL (e.g., http://127.0.0.1:8000/)
    path('', index, name='index'), 
    
    # 2. Login Page: maps to the custom authentication view
    # The trailing slash ('/') is the convention.
    path('login/', custom_admin_login, name='login'),
    path('admin_dashboard/' , admin_dashboard , name='admin_dashboard') 
    
    
    # Optional: You can remove the conflicting and incorrect login path entries.
]