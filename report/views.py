import datetime
import json

from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from report.app.excel import Excel
from report.app.team import TeamUtils
from .models import User, Team, Project

list_info_today = []
list_info_result = []


def login(request):
    return render(request, 'report/login.html')


def logout(request):
    response = HttpResponse(0)
    response.delete_cookie("user")
    return response


def get_projects(request):
    team = request.GET['team']

    try:
        projects = Project.objects.filter(team__name=team)
    except Project.DoesNotExist:
        return HttpResponse(-1)
    return JsonResponse(list(projects.values('id', 'name')), safe=False)


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
        response.set_cookie('team', user.team.name)
        return response
    else:
        return HttpResponse(-2)


def edit(request):
    return render(request, 'report/edit.html')


def get_current_name(request):
    user = request.GET['user']
    date = timezone.now().date()
    try:
        info = User.objects.get(email=user)
        user_info = {"name": info.name, "permission": info.permission}
        daily = TeamUtils.get_team_daily(info.team.name)
        today_info = daily.objects.filter(date=timezone.now().date()).filter(email=user)
        past = daily.objects.filter(email=user).filter(
            date__range=(date - datetime.timedelta(days=3), date - datetime.timedelta(days=1)))
        if today_info.count() == 0:
            user_info['today'] = ""
        else:
            user_info['today'] = list(today_info.values())
        if past.count() == 0:
            user_info['past'] = ""
        else:
            user_info['past'] = list(past.values())
    except User.DoesNotExist:
        return HttpResponse(-1)
    return JsonResponse(user_info)


@csrf_exempt
def send_daily(request):
    try:
        user = User.objects.get(email=request.POST['user'])
        data = json.loads(request.POST['data'])

        len_insert = len(data['insert'])
        len_del = len(data['del'])
        len_modify = len(data['modify']['id'])

        daily = TeamUtils.get_team_daily(user.team.name)

        if len_insert != 0:
            for x in data['insert']:
                user_team = daily()
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
                user_team.email = user.email
                user_team.save()

        if len_del != 0:
            for x in data['del']:
                daily.objects.get(id=x).delete()

        if len_modify != 0:
            for i in range(len_modify):
                daily.objects.filter(id=data['modify']['id'][i]).update(
                    project=data['modify']['data'][i][0],
                    work_type=data['modify']['data'][i][1],
                    bugid=data['modify']['data'][i][2],
                    describe=data['modify']['data'][i][3],
                    priority=data['modify']['data'][i][4],
                    reopen=data['modify']['data'][i][5],
                    reopen_reason=data['modify']['data'][i][6],
                    solution=data['modify']['data'][i][7],
                    solution_reason=data['modify']['data'][i][8],
                    remake=data['modify']['data'][i][11]
                )

    except User.DoesNotExist:
        return HttpResponse(-1)
    except daily.DoesNotExist:
        return HttpResponse(-1)

    return HttpResponse(0)


def statistics(request):
    return render(request, 'report/collect.html')


def collect(request):
    team = request.GET['team']
    list_info_today.clear()
    try:
        daily = TeamUtils.get_team_daily(team)
        today_all = daily.objects.filter(date=timezone.now().date())
        if today_all.count() == 0:
            return HttpResponse(0)
        current_user = [x['email'] for x in today_all.values('email').distinct()]
        team_user = [x.email for x in User.objects.filter(team__name='app')]
        ret_list = []
        for x in list(set(current_user) ^ set(team_user)):
            ret_list.append(User.objects.get(email=x).name)
        for x in today_all.values_list():
            list_info_today.append(list(x)[1:-1])
    except daily.DoesNotExist:
        return HttpResponse(-1)
    info = {'info': list(today_all.values()), 'name': ret_list}
    return JsonResponse(info, safe=False)


def download(request):
    excel = Excel()
    the_file_path = excel.write_to_excel(list_info_today, mark=True)

    def file_iterator(file_name):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read()
                if c:
                    yield c
                else:
                    break

    the_file_name = "daily-%s.xlsx" % timezone.now().date().strftime("%Y-%m-%d")
    response = StreamingHttpResponse(file_iterator(the_file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

    return response


def search(request):
    return render(request, 'report/search.html')


paginator = None


def search_info(request):
    global paginator
    list_info_result.clear()
    info = json.loads(request.GET['data'])
    daily = TeamUtils.get_team_daily(info['team'])
    worktype = info['worktype']
    bugid = info['bugid']
    describe = info['describe']
    solution = info['solution']
    solution_reason = info['solution_reason']
    start_date = info['start_date']
    end_date = info['end_date']
    user = info['user']
    result = daily.objects
    if worktype != "":
        result = result.filter(work_type=worktype)
    if bugid != "":
        result = result.filter(bugid__icontains=bugid)
    if describe != "":
        result = result.filter(describe__icontains=describe)
    if solution != "":
        result = result.filter(solution=solution)
    if solution_reason != "":
        result = result.filter(solution_reason=solution_reason)
    if start_date != "" and end_date != "":
        result = result.filter(date__range=(start_date, end_date))
    if user != "":
        result = result.filter(email=user)

    paginator = Paginator(result, 20)
    for x in result.values_list():
        list_info_result.append(list(x)[1:-1])

    if result.count() == 0:
        return HttpResponse(0)
    return JsonResponse({"data": list(paginator.page(1).object_list.values()), "pages": paginator.num_pages}, safe=False)


def move_page(request):
    global paginator
    page = request.GET["page"]
    return JsonResponse(list(paginator.page(page).object_list.values()), safe=False)


def download_search(request):
    excel = Excel()
    the_file_path = excel.write_to_excel(list_info_result)

    def file_iterator(file_name):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read()
                if c:
                    yield c
                else:
                    break

    the_file_name = "search-%s.xlsx" % timezone.now().date().strftime("%Y-%m-%d")
    response = StreamingHttpResponse(file_iterator(the_file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

    return response


def today(request):
    return render(request, 'report/today.html')


def settings(request):
    return render(request, 'report/team_setting.html')


def get_team_user(request):
    team = request.GET['team']

    try:
        users = User.objects.filter(team__name=team)

    except User.DoesNotExist:
        return HttpResponse(-1)

    return JsonResponse(list(users.values()), safe=False)


@csrf_exempt
def insert_user(request):
    user = json.loads(request.POST['data'])
    try:
        new_user = User()
        new_user.name = user["name"]
        new_user.email = user["email"]
        new_user.pwd = user["pwd"]
        new_user.team = Team.objects.get(name=user["team"])
        new_user.save()
    except User.DoesNotExist:
        return HttpResponse(-1)

    return HttpResponse(new_user.id)


@csrf_exempt
def modify_user(request):
    user = json.loads(request.POST['data'])
    try:
        length_modify = len(user['modify']['id'])

        if len(user['del']) != 0:
            for x in user['del']:
                User(id=x).delete()
        if length_modify != 0:
            for i in range(length_modify):
                user = User.objects.filter(id=user['modify']['id'][i]).update(
                    permission=user['modify']['permission'][i])
    except User.DoesNotExist:
        return HttpResponse(-1)
    return HttpResponse(0)


@csrf_exempt
def delete_projects(request):
    ids = json.loads(request.POST['data'])
    try:
        for x in ids:
            Project.objects.get(id=x).delete()
    except Project.DoesNotExist:
        return HttpResponse(-1)
    return HttpResponse(0)


@csrf_exempt
def insert_project(request):
    team = request.POST['team']
    data = request.POST['data']
    try:
        project = Project()
        project.name = data
        project.team = Team.objects.get(name=team)
        project.save()
    except Project.DoesNotExist:
        return HttpResponse(-1)
    return HttpResponse(project.id)
