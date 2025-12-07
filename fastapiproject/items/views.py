
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login 
from django.conf import settings
from .models import Admin , Item , User , RequestItem

def index(request):
    return render(request, 'user_login.html')


def admin_dashboard(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('custom_admin_login')  

    # Get admin object
    admin = Admin.objects.get(admin_id=admin_id)

    get_admin_items = Item.objects.filter(admin_id=admin)
    get_admin_items_count = get_admin_items.count()

    users = User.objects.all()

    requests = RequestItem.objects.all()


    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        item_amount = request.POST.get('item_amount')

        if item_name and item_amount:
            Item.objects.create(item_name=item_name, item_amount=item_amount, admin_id=admin)
            return redirect('admin_dashboard')
        

    return render(request, 'admin_dashboard.html', {'admin': admin,'get_admin_items_count': get_admin_items_count,'get_admin_items': get_admin_items,'users': users, 'requests': requests,
    })


def approve_request(request,request_id):
    try:
        request_item = RequestItem.objects.get(request_id=request_id)
        request_item.status = 'Approved'
        request_item.save()
        return redirect('admin_dashboard')
    except RequestItem.DoesNotExist:
        return redirect('admin_dashboard')
    

def admin_logout(request):
    request.session.flush()
    return redirect('custom_admin_login')

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
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    user = User.objects.get(user_id=user_id)
    return render(request , 'reserve.html', {'user': user})


def register_user(request):

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')

        user = User(full_name=full_name , student_id=student_id , password=password)
        user.save()

        return redirect(reserve_page)
    return render(request , 'user_register.html')


def user_login(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')

        try:
             user = User.objects.get(student_id=student_id , password=password)
             request.session['user_id'] = user.user_id
             return redirect(dashboard_home)

        except User.DoesNotExist:
             print("Invalid user credentials")
             return render(request , 'user_login.html')

    return render(request , 'user_login.html')


def user_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    user = User.objects.get(user_id=user_id)
    return render(request , 'dashboard_home.html', {'user': user})


def user_dashboard2(request):
    return redirect('dashboard_home')


def dashboard_home(request):
    # Ensure user is logged in
    user_id = request.session.get('user_id')

    requestitem = RequestItem.objects.filter(user_id=user_id)

    if not user_id:
        return redirect('user_login')
        
    user = User.objects.get(user_id=user_id)
    return render(request , 'dashboard_home.html', {'user': user, 'requestitem': requestitem})

def reserve_item(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    items = Item.objects.all()
    
        
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        item_amount = request.POST.get('item_amount')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        user = User.objects.get(user_id=user_id)
        
        RequestItem.objects.create(
            user_id=user,
            item_name=item_name,
            item_amount=item_amount,
            request_date=date,
            time_requested=time
        )

        print(f"Reservation Request: {item_name} x{item_amount} on {date}")
        return redirect('dashboard_home')
        
    return render(request, 'form_reserve_item.html' , {'items' : items})

def reserve_lab(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
        
    if request.method == 'POST':
        lab_name = request.POST.get('lab_name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        # Save lab booking logic here
        print(f"Lab Booking: {lab_name} on {date} at {time}")
        return redirect('dashboard_home')
        
    return render(request, 'form_reserve_lab.html')

def logout_view(request):
    request.session.flush()
    return redirect('user_login')