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

            try:
                user = User.objects.get(username=u_name)
                agency = user.agency.name
                print(agency)
            except:
                request.session.clear()
                return redirect(reverse('login'))

            if user.username == u_name and user.password == p_word:
                create_session(request, u_name, agency)
                return redirect(reverse('observer:home'))

    return render(request, 'role_management/login.html')


def create_session(request, username, agency):
    request.session['username'] = username
    request.session['agency'] = agency


def delete_session(request):
    request.session.flush()
    request.session.clear_expired()
    return redirect(log_in)


def logout_request(request):
    delete_session(request)
    return redirect(log_in)


def registration(request):
    agencies = Agency.objects.all()

    context = {
        'agencies': agencies,
    }

    if request.method == 'POST':
        print(request.POST)

        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            user = User(username=username, password=password,
                        agency=Agency.objects.get(name=request.POST['agency']))
            user.save()
            return redirect(reverse('login'))

    print("usertype print korchi")

    return render(request, 'role_management/registration.html', context)


def test(request):
    return render(request, 'role_management/login-2.html')