# Assuming your views.py has:
# from .views import index, custom_admin_login

from django.urls import path
from .views import index, custom_admin_login , admin_dashboard , reserve_page , insert_admin , register_user

urlpatterns = [
    # 1. Homepage: maps the root URL (e.g., http://127.0.0.1:8000/)
    path('', index, name='index'), 
    
    # 2. Login Page: maps to the custom authentication view
    # The trailing slash ('/') is the convention.
    path('login/', custom_admin_login, name='login'),
    path('admin_dashboard/' , admin_dashboard , name='admin_dashboard') ,
    path('reserve/' , reserve_page , name='reserve'),
    path('insert_admin/' , insert_admin , name='insert_admin') ,
    path('register_user/' , register_user , name='register_user')
]