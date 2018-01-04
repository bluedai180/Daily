import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render

from .models import User, Team, AppDaily
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import datetime
import json


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
        response.set_cookie('user', id)
        return response
    else:
        return HttpResponse(-2)


def edit(request):
    return render(request, 'report/edit.html')


def get_last_info(request):
    user = request.GET['user']
    date = timezone.now().date()
    try:
        info = AppDaily.objects.filter(email=user).filter(
            date__range=(date - datetime.timedelta(days=3), date - datetime.timedelta(days=1)))
    except AppDaily.DoesNotExist:
        return HttpResponse("have not last info")
    if len(info) == 0:
        return HttpResponse("qqqqqqq")
    return JsonResponse(list(info.values()), safe=False)


def get_current_name(request):
    user = request.GET['user']
    try:
        info = User.objects.get(email=user)
    except User.DoesNotExist:
        return HttpResponse("have not this user")
    return HttpResponse(info.name)


@csrf_exempt
def post_daily(request):
    user = request.POST['user']
    data = request.POST['data']
    try:
        team = User.objects.get(email=user)
        info = json.loads(data)
        if team.team.name == "app":
            print("111111111")
        for x in info:
            user_team = AppDaily()
            user_team.project = x[0]
            user_team.work_type = x[1]
            user_team.bugid = x[2]
            user_team.describe = x[3]
            user_team.priority = x[4]
            user_team.reopen = x[5]
            user_team.reopen_reason = x[6]
            user_team.solution = x[7]
            user_team.solution_reason = x[8]
            user_team.person = x[9]
            user_team.date = datetime.datetime.strptime(x[10], "%Y-%m-%d")
            user_team.remake = x[11]
            user_team.email = user
            user_team.save()

    except User.DoesNotExist:
        return HttpResponse("have not this user")

    return HttpResponse("app team")
