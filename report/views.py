from django.shortcuts import render

from .models import User, Team, AppDaily
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


def login(request):
    return render(request, 'report/login.html')


def check_user(request):
    id = request.GET['id']
    pwd = request.GET['pwd']
    try:
        user = User.objects.get(email=id)
    except User.DoesNotExist:
        return HttpResponse(-1)
    if user.pwd == pwd:
        response = HttpResponse(0)
        response.set_cookie('user', id, 3600)
        return response
    else:
        return HttpResponse(-2)


def edit(request):
    return render(request, 'report/edit.html')
