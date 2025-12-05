
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login 
from django.conf import settings
from .models import Admin , Item

def index(request):
    return render(request, 'login.html')


def admin_dashboard(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('custom_admin_login')  

    admin = Admin.objects.get(admin_id=admin_id)

    get_admin_items = Item.objects.filter(admin_id = admin)

    get_admin_items_count = get_admin_items.count()
    

    

    if request.method == 'POST':
      item_name = request.POST.get('item_name')
      item_amount = request.POST.get('item_amount')

      Item.objects.create(item_name=item_name, item_amount=item_amount, admin_id=admin)

    # Re-fetch items and count after creation
      get_admin_items = Item.objects.filter(admin_id=admin)
      get_admin_items_count = get_admin_items.count()

      return redirect('admin_dashboard' )

    

    return render(request, 'admin_dashboard.html', {'admin': admin , 'get_admin_items_count' : get_admin_items_count , 'get_admin_items' : get_admin_items} )


def insert_admin(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        admin_password = request.POST.get('admin_password')

        admin = Admin(staff_id=staff_id , admin_password=admin_password)
        admin.save()

        success_message = f"Admin with Staff ID '{staff_id}' added successfully!"
        return render(request, 'admin_dashboard.html', {'success': success_message})

    return render(request , 'insert_admin.html')




def custom_admin_login(request):
    if request.method == 'POST':
        admin_password = request.POST.get('admin_password')
        staff_id = request.POST.get('staff_id')

        try:
              admin = Admin.objects.get(staff_id=staff_id, admin_password=admin_password)
              request.session['admin_id'] = admin.admin_id
              return redirect('admin_dashboard')
        

        except Admin.DoesNotExist:
              print("Invalid credentials")
              return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def reserve_page(request):
    return render(request , 'reserve.html')