# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from .forms import RegisterForm

# def register_view(request):
#     form = RegisterForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('login')
#     return render(request, 'register.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         user = authenticate(
#             email=request.POST['email'],
#             password=request.POST['password']
#         )
#         if user:
#             login(request, user)
#             return redirect('user_list')
#     return render(request, 'login.html')

# def logout_view(request):
#     logout(request)
#     return redirect('login')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib import messages
from .forms import RegisterForm

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Account created successfully")
        return redirect('login')
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            user.is_online = True
            user.save()
            return redirect('user_list')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')

def logout_view(request):
    if request.user.is_authenticated:
        request.user.is_online = False
        request.user.last_seen = timezone.now()
        request.user.save()
    logout(request)
    return redirect('login')