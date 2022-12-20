import string

from django.urls import reverse

from .models import *
from django.shortcuts import render, redirect
from rest_framework.response import Response


def log_in(request):
    if 'username' in request.session:
        return redirect(reverse('observer:home'))
    else:
        if request.method == "POST":

            u_name = request.POST['username']
            p_word = request.POST['password']
            role = ''

            try:
                user = User.objects.get(username=u_name)
                role = user.userType.code
            except:
                request.session.clear()
                return redirect(reverse('login'))

            if user.username == u_name and user.password == p_word:
                create_session(request, u_name, role)
                return redirect(reverse('observer:home'))

    return render(request, 'role_management/login.html')


def create_session(request, username, role):
    request.session['username'] = username
    request.session['role'] = role


def delete_session(request):
    request.session.flush()
    request.session.clear_expired()
    return redirect(log_in)


def logout_request(request):
    delete_session(request)
    return redirect(log_in)


def registration(request):
    userTypes = Agency.objects.all()

    context = {
        'userTypes': userTypes,
    }

    if request.method == 'POST':
        print(request.POST)

        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            user = User(username=username, password=password,
                        userType=UserTypes.objects.get(code=request.POST['userType']))
            user.save()


            return redirect(reverse('login'))

    print("usertype print korchi")
    print(userTypes)

    return render(request, 'role_management/registration.html', context)
