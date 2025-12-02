# items/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.conf import settings

def index(request):
    return render(request, 'login.html')


def custom_admin_login(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')
        special_id = request.POST.get('special_id')

        # 3. Authenticate against the username and password
        user = authenticate(request, username=student_id, password=password)

        if user is not None:
            # User is authenticated by Django
            
            if special_id == 'STEMFUN2024':
                login(request, user)
                
                print("Login successful for user: " , user.username)
                return redirect(settings.LOGIN_REDIRECT_URL)
                
            else:
                # Custom check failed
                print("Invalid Special Student ID attempt for user: ", user.username)
                error_message = 'Invalid Special Student ID.'
        else:
            # 6. Explicitly handle failed Django authentication
            error_message = 'Invalid Student ID or Password.'
            print(error_message)
        
        # If authentication or custom check failed, re-render the form with error
        return render(request, 'login.html', {'error': error_message})
        
    else:
        # GET request: just display the empty form
        return render(request, 'login.html')