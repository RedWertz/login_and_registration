from django.shortcuts import render, redirect
from .models import users
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'GET':
        return redirect('/login')
    errors = users.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/login')
    else:
        new_user = users.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered")
        return redirect('/sucess')

def login(request):
    if request.method == 'GET':
        return redirect('/login')
    if not users.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, "Invalid Username/Password")
        return redirect('/login')
    user = users.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in")
    return redirect('/login/success')

def logout(request):
    request.session.clear()
    return redirect('/login')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    user = users.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'successful_login.html', context)

