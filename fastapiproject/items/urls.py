# Assuming your views.py has:
# from .views import index, custom_admin_login

from django.urls import path
from .views import (
    index, 
    custom_admin_login, 
    admin_dashboard, 
    reserve_page, 
    insert_admin, 
    register_user, 
    user_login, 
    user_dashboard, 
    user_dashboard2, 
    dashboard_home, 
    reserve_item, 
    reserve_lab ,
    approve_request,
    admin_logout,
)

urlpatterns = [
    # 1. Homepage: maps the root URL
    path('', index, name='index'), 
    
    # Auth & Admin
    path('adminlogin/', custom_admin_login, name='custom_admin_login'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('insert_admin/', insert_admin, name='insert_admin'),
    
    # User Auth
    path('register_user/', register_user, name='register_user'),
    path('user_login/', user_login, name='user_login'),
    
    # Legacy / Redirects (kept for compatibility or redirected in views)
    path('user_dashboard/', user_dashboard, name='user_dashboard'), 
    path('user_dashboard2/', user_dashboard2, name='user_dashboard2'),
    path('reserve/', reserve_page, name='reserve'),
    path('approve_request/<int:request_id>/', approve_request, name='approve_request'),
    path('admin_logout/', admin_logout, name='admin_logout'),

    # New Static Dashboard
    path('dashboard/', dashboard_home, name='dashboard_home'),
    path('dashboard/reserve-item/', reserve_item, name='reserve_item'),
    path('dashboard/reserve-lab/', reserve_lab, name='reserve_lab'),
]
