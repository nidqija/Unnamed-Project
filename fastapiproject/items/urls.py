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
    approve_venue_request,
    admin_logout,
    bookmark_material,
    remove_bookmark,
    browse_materials,
    delete_item,
    delete_venue,
    mark_as_returned,
    venue_availability,
)

urlpatterns = [
    path('', index, name='index'), 
    
    path('adminlogin/', custom_admin_login, name='custom_admin_login'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('insert_admin/', insert_admin, name='insert_admin'),
    
    path('register_user/', register_user, name='register_user'),
    path('user_login/', user_login, name='user_login'),
    
    path('user_dashboard/', user_dashboard, name='user_dashboard'), 
    path('user_dashboard2/', user_dashboard2, name='user_dashboard2'),
    path('reserve/', reserve_page, name='reserve'),
    path('approve_request/<int:request_id>/', approve_request, name='approve_request'),
    path('approve_venue_request/<int:request_id>/', approve_venue_request, name='approve_venue_request'),
    path('delete_item/<int:item_id>/', delete_item, name='delete_item'),
    path('delete_venue/<int:lab_id>/', delete_venue, name='delete_venue'),
    path('mark_returned/<str:request_type>/<int:request_id>/', mark_as_returned, name='mark_as_returned'),
    path('admin_logout/', admin_logout, name='admin_logout'),

    path('dashboard/', dashboard_home, name='dashboard_home'),
    path('dashboard/reserve-item/', reserve_item, name='reserve_item'),
    path('dashboard/reserve-lab/', reserve_lab, name='reserve_lab'),
    path('dashboard/browse-materials/', browse_materials, name='browse_materials'),
    path('dashboard/venue-availability/', venue_availability, name='venue_availability'),
    path('bookmark/<int:material_id>/', bookmark_material, name='bookmark_material'),
    path('remove-bookmark/<int:bookmark_id>/', remove_bookmark, name='remove_bookmark'),
]
