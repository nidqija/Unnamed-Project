
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.conf import settings

def index(request):
    return render(request, 'login.html')


def admin_dashboard(request):
    return render(request , 'admin_dashboard.html')



def custom_admin_login(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')
        special_id = request.POST.get('special_id')

        user = authenticate(request, username=student_id, password=password)

        if user is not None:
            
            if special_id == 'STEMFUN2024':
                login(request, user)
                
                print("Login successful for user: " , user.username)
                return redirect(settings.LOGIN_REDIRECT_URL)
                
            else:
                print("Invalid Special Student ID attempt for user: ", user.username)
                error_message = 'Invalid Special Student ID.'
        else:
            error_message = 'Invalid Student ID or Password.'
            print(error_message)
        
        return render(request, 'login.html', {'error': error_message})
        
    else:
        return render(request, 'login.html')