
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login 
from django.conf import settings
from .models import Admin , Item , User , RequestItem, Lab, RequestVenue, Material, Bookmark, Fine
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

def index(request):
    return render(request, 'user_login.html')


def admin_dashboard(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('custom_admin_login')  

    admin = Admin.objects.get(admin_id=admin_id)

    get_admin_items = Item.objects.filter(admin_id=admin)
    get_admin_items_count = get_admin_items.count()
    
    get_admin_labs = Lab.objects.filter(admin_id=admin)
    get_admin_labs_count = get_admin_labs.count()
    
    get_admin_materials = Material.objects.filter(admin_id=admin)
    get_admin_materials_count = get_admin_materials.count()

    users = User.objects.all()
    users_count = users.count()

    requests = RequestItem.objects.all()
    venue_requests = RequestVenue.objects.all()
    
    calculate_fines()
    
    all_fines = Fine.objects.all()
    unpaid_fines = Fine.objects.filter(status='Unpaid')
    total_fines_amount = sum([fine.fine_amount for fine in unpaid_fines])
    
    active_sessions = RequestVenue.objects.filter(status='Approved').count()
    
    items = Item.objects.all()
    inventory_data = {}
    for item in items:
        category = item.item_name.split()[0] if item.item_name else 'Other'
        if category not in inventory_data:
            inventory_data[category] = 0
        inventory_data[category] += item.item_amount
    
    materials = Material.objects.all()
    bookmarks_count = Bookmark.objects.count()

    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        item_amount = request.POST.get('item_amount')
        lab_name = request.POST.get('lab_name')
        lab_location = request.POST.get('lab_location')
        lab_capacity = request.POST.get('lab_capacity')
        material_title = request.POST.get('material_title')
        material_author = request.POST.get('material_author')
        material_category = request.POST.get('material_category')
        material_description = request.POST.get('material_description')
        material_isbn = request.POST.get('material_isbn')

        if item_name and item_amount:
            Item.objects.create(item_name=item_name, item_amount=item_amount, admin_id=admin)
            return redirect('admin_dashboard')
        
        if lab_name:
            Lab.objects.create(
                lab_name=lab_name, 
                location=lab_location or '', 
                capacity=int(lab_capacity) if lab_capacity else 1,
                admin_id=admin
            )
            return redirect('admin_dashboard')
        
        if material_title:
            Material.objects.create(
                title=material_title,
                author=material_author or '',
                category=material_category or '',
                description=material_description or '',
                isbn=material_isbn or '',
                admin_id=admin
            )
            return redirect('admin_dashboard')
        

    return render(request, 'admin_dashboard.html', {
        'admin': admin,
        'get_admin_items_count': get_admin_items_count,
        'get_admin_items': get_admin_items,
        'get_admin_labs_count': get_admin_labs_count,
        'get_admin_labs': get_admin_labs,
        'get_admin_materials_count': get_admin_materials_count,
        'users_count': users_count,
        'active_sessions': active_sessions,
        'inventory_data': inventory_data,
        'materials': materials,
        'bookmarks_count': bookmarks_count,
        'users': users, 
        'requests': requests,
        'venue_requests': venue_requests,
        'all_fines': all_fines,
        'unpaid_fines': unpaid_fines,
        'total_fines_amount': total_fines_amount,
    })


def approve_request(request, request_id):
    try:
        request_item = RequestItem.objects.get(request_id=request_id)
        item = Item.objects.filter(item_name=request_item.item_name).first()
        
        if item is None:
            request_item.status = 'Rejected'
        elif item.item_amount >= request_item.item_amount:
            item.item_amount -= request_item.item_amount
            item.save()
            request_item.status = 'Approved'
            if not request_item.return_date:
                request_item.return_date = request_item.request_date + timedelta(days=7)
        else:
            request_item.status = 'Rejected'

        request_item.save()
    except RequestItem.DoesNotExist:
        pass

    return redirect('admin_dashboard')

def approve_venue_request(request, request_id):
    try:
        venue_request = RequestVenue.objects.get(request_id=request_id)
        status = request.POST.get('status', 'Approved')
        venue_request.status = status
        
        if status == 'Approved' and not venue_request.return_date:
            venue_request.return_date = venue_request.request_date + timedelta(days=7)
        
        venue_request.save()
    except RequestVenue.DoesNotExist:
        pass

    return redirect('admin_dashboard')

def delete_item(request, item_id):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('custom_admin_login')
    
    try:
        item = Item.objects.get(item_id=item_id, admin_id=admin_id)
        item.delete()
    except Item.DoesNotExist:
        pass
    
    return redirect('admin_dashboard')

def delete_venue(request, lab_id):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('custom_admin_login')
    
    try:
        lab = Lab.objects.get(lab_id=lab_id, admin_id=admin_id)
        lab.delete()
    except Lab.DoesNotExist:
        pass
    
    return redirect('admin_dashboard')

def calculate_fines():
    today = timezone.now().date()
    
    overdue_items = RequestItem.objects.filter(
        status='Approved',
        return_date__lt=today,
        actual_return_date__isnull=True
    )
    
    for item_request in overdue_items:
        existing_fine = Fine.objects.filter(
            request_item=item_request,
            status='Unpaid'
        ).first()
        
        if not existing_fine:
            days_overdue = (today - item_request.return_date).days
            fine_amount = Decimal(days_overdue * 5.00)
            
            Fine.objects.create(
                user_id=item_request.user_id,
                request_item=item_request,
                fine_amount=fine_amount,
                fine_reason=f'Overdue item return - {days_overdue} days late'
            )
    
    overdue_venues = RequestVenue.objects.filter(
        status='Approved',
        return_date__lt=today,
        actual_return_date__isnull=True
    )
    
    for venue_request in overdue_venues:
        existing_fine = Fine.objects.filter(
            request_venue=venue_request,
            status='Unpaid'
        ).first()
        
        if not existing_fine:
            days_overdue = (today - venue_request.return_date).days
            fine_amount = Decimal(days_overdue * 10.00)
            
            Fine.objects.create(
                user_id=venue_request.user_id,
                request_venue=venue_request,
                fine_amount=fine_amount,
                fine_reason=f'Overdue venue return - {days_overdue} days late'
            )

def mark_as_returned(request, request_type, request_id):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('custom_admin_login')
    
    today = timezone.now().date()
    
    if request_type == 'item':
        try:
            item_request = RequestItem.objects.get(request_id=request_id)
            item_request.actual_return_date = today
            item_request.status = 'Returned'
            
            item = Item.objects.filter(item_name=item_request.item_name).first()
            if item:
                item.item_amount += item_request.item_amount
                item.save()
            
            item_request.save()
            
            Fine.objects.filter(
                request_item=item_request,
                status='Unpaid'
            ).update(status='Paid', paid_date=today)
            
        except RequestItem.DoesNotExist:
            pass
    
    elif request_type == 'venue':
        try:
            venue_request = RequestVenue.objects.get(request_id=request_id)
            venue_request.actual_return_date = today
            venue_request.status = 'Returned'
            venue_request.save()
            
            Fine.objects.filter(
                request_venue=venue_request,
                status='Unpaid'
            ).update(status='Paid', paid_date=today)
            
        except RequestVenue.DoesNotExist:
            pass
    
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
    user_id = request.session.get('user_id')

    requestitem = RequestItem.objects.filter(user_id=user_id)
    requestvenue = RequestVenue.objects.filter(user_id=user_id)
    
    user_bookmarks = Bookmark.objects.filter(user_id=user_id).select_related('material_id')
    
    materials = Material.objects.all()
    
    user_fines = Fine.objects.filter(user_id=user_id, status='Unpaid')
    user_total_fines = sum([fine.fine_amount for fine in user_fines])

    if not user_id:
        return redirect('user_login')
        
    user = User.objects.get(user_id=user_id)
    return render(request , 'dashboard_home.html', {
        'user': user, 
        'requestitem': requestitem,
        'requestvenue': requestvenue,
        'user_bookmarks': user_bookmarks,
        'materials': materials,
    })

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
    
    labs = Lab.objects.all()
        
    if request.method == 'POST':
        lab_name = request.POST.get('lab_name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        user = User.objects.get(user_id=user_id)
        try:
            admin = Admin.objects.get(admin_id=1)
        except Admin.DoesNotExist:
            admin = Admin.objects.first()
            if not admin:
                return redirect('dashboard_home')
        
        RequestVenue.objects.create(
            user_id=user,
            venue_name=lab_name,
            request_date=date,
            time_requested=time,
            admin_id=admin
        )
        
        return redirect('dashboard_home')
        
    return render(request, 'form_reserve_lab.html', {'labs': labs})

def bookmark_material(request, material_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    try:
        user = User.objects.get(user_id=user_id)
        material = Material.objects.get(material_id=material_id)
        
        bookmark, created = Bookmark.objects.get_or_create(
            user_id=user,
            material_id=material
        )
        
        if created:
            return redirect('dashboard_home')
        else:
            bookmark.delete()
            return redirect('dashboard_home')
    except Material.DoesNotExist:
        return redirect('dashboard_home')

def remove_bookmark(request, bookmark_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    try:
        bookmark = Bookmark.objects.get(bookmark_id=bookmark_id, user_id=user_id)
        bookmark.delete()
    except Bookmark.DoesNotExist:
        pass
    
    return redirect('dashboard_home')

def browse_materials(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    materials = Material.objects.all()
    user = User.objects.get(user_id=user_id)
    
    bookmarked_ids = list(Bookmark.objects.filter(user_id=user).values_list('material_id', flat=True))
    
    return render(request, 'browse_materials.html', {
        'materials': materials,
        'user': user,
        'bookmarked_ids': bookmarked_ids,
    })

def venue_availability(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    user = User.objects.get(user_id=user_id)
    labs = Lab.objects.all()
    
    approved_venues = RequestVenue.objects.filter(status='Approved')
    
    availability_data = []
    today = timezone.now().date()
    
    time_slots = [
        ('09:00', '09:00 - 11:00'),
        ('11:00', '11:00 - 13:00'),
        ('14:00', '14:00 - 16:00'),
        ('16:00', '16:00 - 18:00')
    ]
    
    for lab in labs:
        lab_data = {
            'lab': lab,
            'days': []
        }
        
        for day_offset in range(7):
            check_date = today + timedelta(days=day_offset)
            day_slots = []
            
            for time_code, time_display in time_slots:
                is_booked = approved_venues.filter(
                    venue_name=lab.lab_name,
                    request_date=check_date,
                    time_requested=time_code
                ).exists()
                
                day_slots.append({
                    'time_code': time_code,
                    'time_display': time_display,
                    'available': not is_booked
                })
            
            lab_data['days'].append({
                'date': check_date,
                'slots': day_slots
            })
        
        availability_data.append(lab_data)
    
    return render(request, 'venue_availability.html', {
        'user': user,
        'availability_data': availability_data,
        'labs': labs,
        'today': today,
    })

def logout_view(request):
    request.session.flush()
    return redirect('user_login')