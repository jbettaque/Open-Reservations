from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Username or Password is incorrect.'})
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return redirect('home')


def register(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password_confirm']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/register.html', {'error': 'Username is already taken :('})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'accounts/register.html', {'error': "Password's didn't match :("})

    else:
        pass
        # TODO
    return render(request, 'accounts/register.html')

