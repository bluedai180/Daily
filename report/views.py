import datetime
import json
import svn.local
import svn.exception

from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta
from itertools import chain

from report.app.excel import Excel
from report.app.team import TeamUtils
from .models import User, Team, Project

list_info_today = []
list_info_result = []


def login(request):
    return render(request, 'report/login.html')


# 10.10.152.66/api/logout
def logout(request):
    response = HttpResponse(0)
    response.delete_cookie("user")
    response.delete_cookie("team")
    return response


# 10.10.152.66/api/projects
def get_projects(request):
    team = request.GET['team']
    total = request.GET['total']
    try:
        if team == "director":
            projects = Project.objects.all()
            return JsonResponse(list(projects.values('id', 'company', 'name')), safe=False)
        else:
            if total == "true":
                projects = Project.objects.all()
                return JsonResponse(list(projects.values('id', 'name', team)), safe=False)
            else:
                projects = TeamUtils.get_team_select_projects(team)
                return JsonResponse(list(projects.values('id', 'name', team)), safe=False)
    except Project.DoesNotExist:
        return HttpResponse(-1)


# 10.10.152.66/api/login
def check_user(request):
    id = request.GET['id']
    pwd = request.GET['pwd']
    is_remember = request.GET['remember']
    try:
        user = User.objects.get(email=id)
    except User.DoesNotExist:
        return HttpResponse(-1)
    if user.pwd == pwd:
        if user.is_manager():
            response = HttpResponse(1)
        else:
            response = HttpResponse(0)
        if is_remember == "true":
            response.set_cookie('user', id, max_age=60 * 60 * 24 * 30)
            response.set_cookie('team', user.team.name, max_age=60 * 60 * 24 * 30)
        else:
            response.set_cookie('user', id)
            response.set_cookie('team', user.team.name)
        return response
    else:
        return HttpResponse(-2)


def edit(request):
    return render(request, 'report/edit.html')


def manage(request):
    return render(request, 'report/manage.html')


# 10.10.152.66/api/user
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


# 10.10.152.66/api/daily
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
                user_team.person = user.name
                user_team.date = datetime.datetime.now().strftime("%Y-%m-%d")
                user_team.remake = x[9]
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
                    remake=data['modify']['data'][i][9]
                )

    except User.DoesNotExist:
        return HttpResponse(-1)
    except daily.DoesNotExist:
        return HttpResponse(-1)

    return HttpResponse(0)


def statistics(request):
    return render(request, 'report/collect.html')


# 10.10.152.66/api/daily/today
def collect(request):
    team = request.GET['team']
    list_info_today.clear()
    try:
        daily = TeamUtils.get_team_daily(team)
        today_all = daily.objects.filter(date=timezone.now().date())
        if today_all.count() == 0:
            return HttpResponse(0)
        current_user = [x['email'] for x in today_all.values('email').distinct()]
        team_user = [x.email for x in User.objects.filter(team__name=team)]
        ret_list = []
        for x in list(set(current_user) ^ set(team_user)):
            ret_list.append(User.objects.get(email=x).name)
        for x in today_all.values_list():
            list_info_today.append(list(x)[1:-1])
    except daily.DoesNotExist:
        return HttpResponse(-1)
    info = {'info': list(today_all.values()), 'name': ret_list}
    return JsonResponse(info, safe=False)


@csrf_exempt
def download(request):
    excel = Excel()
    team = request.POST["team"]
    data = json.loads(request.POST["data"])

    the_file_path = excel.write_to_excel(data, mark=True)

    def file_iterator(file_name):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read()
                if c:
                    yield c
                else:
                    break

    the_file_name = "daily-%s-%s.xlsx" % (team, timezone.now().date().strftime("%Y-%m-%d"))
    response = StreamingHttpResponse(file_iterator(the_file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

    return response


def search(request):
    return render(request, 'report/search.html')


def manage_search(request):
    return render(request, 'report/manage_search.html')


paginator = None


# 10.10.152.66/api/search/daily
def search_info(request):
    global paginator
    list_info_result.clear()
    info = json.loads(request.GET['data'])
    team = info['team']
    project = info['project']
    worktype = info['worktype']
    bugid = info['bugid']
    describe = info['describe']
    solution = info['solution']
    solution_reason = info['solution_reason']
    start_date = info['start_date']
    end_date = info['end_date']
    user = info['user']

    if team != "director":
        daily = TeamUtils.get_team_daily(team)
        result = daily.objects
    else:
        if user == "":
            daily = TeamUtils.get_team_daily(team)
            data = []
            for x in daily:
                result = x.objects
                if project != "":
                    result = result.filter(project=project)
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
                if result.exists():
                    data.extend(list(result.values()))
                    for y in result.values_list():
                        list_info_result.append(list(y)[1:-1])

            paginator = Paginator(data, 20)
            if len(data) == 0:
                return HttpResponse(0)
            return JsonResponse({"data": paginator.page(1).object_list, "pages": paginator.num_pages},
                                safe=False)

        else:
            daily = TeamUtils.get_team_daily(User.objects.get(email=user + "@hipad.com").team.name)
            result = daily.objects
            result = result.filter(email=user + "@hipad.com")

    if project != "":
        result = result.filter(project=project)
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
        result = result.filter(email=user + "@hipad.com")

    paginator = Paginator(list(result.values()), 20)
    for x in result.values_list():
        list_info_result.append(list(x)[1:-1])

    if result.count() == 0:
        return HttpResponse(0)
    return JsonResponse({"data": paginator.page(1).object_list, "pages": paginator.num_pages},
                        safe=False)


def move_page(request):
    global paginator
    page = request.GET["page"]
    return JsonResponse(paginator.page(page).object_list, safe=False)


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


def manage_project(request):
    return render(request, 'report/manage_project.html')


# 10.10.152.66/api/user
def get_team_user(request):
    team = request.GET['team']

    try:
        users = User.objects.filter(team__name=team)

    except User.DoesNotExist:
        return HttpResponse(-1)

    return JsonResponse(list(users.values()), safe=False)


# 10.10.152.66/api/user
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


# 10.10.152.66/api/user
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


# 10.10.152.66/api/projects
@csrf_exempt
def delete_projects(request):
    ids = json.loads(request.POST['data'])
    try:
        for x in ids:
            Project.objects.get(id=x).delete()
    except Project.DoesNotExist:
        return HttpResponse(-1)
    return HttpResponse(0)


# 10.10.152.66/api/projects
@csrf_exempt
def insert_project(request):
    name = request.POST['project']
    company = request.POST['company']
    try:
        project = Project()
        project.name = name
        project.company = company
        project.save()
    except Project.DoesNotExist:
        return HttpResponse(-1)
    return HttpResponse(project.id)


@csrf_exempt
def select_project(request):
    """
    每个部门选择项目总表中的项目，作为日报的项目名下拉菜单的选项，此功能面向部长权限
    :param request:
    :return:
    """
    team = request.POST['team']
    data = json.loads(request.POST['data'])

    try:
        for i in range(len(data['id'])):
            project = Project.objects.get(id=data['id'][i])
            project.__dict__[team] = data['checked'][i]
            project.save()
    except Project.DoesNotExist:
        return HttpResponse(-1)
    return HttpResponse(0)


def edit_weekly(request):
    return render(request, 'report/edit_weekly.html')


# 10.10.152.66/api/user
def get_permission(request):
    try:
        user = User.objects.get(email=request.GET['user'])
    except User.DoesNotExist:
        return HttpResponse(-1)
    return HttpResponse(user.permission)


# 10.10.152.66/api/weekly
def get_weekly_saved(request):
    """
    获取组员已保存的周报
    :param request:
    :return:
    """
    user = request.GET['user']
    team = request.GET['team']
    try:
        weekly = TeamUtils.get_team_weekly(team)
        result = weekly.objects.filter(date__week=datetime.datetime.now().isocalendar()[1]).filter(email=user).filter(
            total=False)
        if result.exists() is False:
            return HttpResponse(0)
    except weekly.DoesNotExist:
        return HttpResponse(-1)
    return JsonResponse(list(result.values()), safe=False)


# 10.10.152.66/api/daily/<start>/<end>
def get_weekly(request):
    """
    获取指定组员，指定日期范围的日报汇总
    :param request:
    :return:
    """
    user = request.GET['user']
    start = request.GET['start']
    end = request.GET['end']
    daily = TeamUtils.get_team_daily(request.GET['team'])
    try:
        result = daily.objects.filter(date__range=(start, end)).filter(email=user)
        total = result.values_list("project", "describe")
        project = list(set([x[0] for x in total]))
        info = [[] for _ in range(len(project))]

        for x in total:
            if x[0] in project:
                if len(info[project.index(x[0])]) == 0:
                    info[project.index(x[0])] = x[1]
                else:
                    info[project.index(x[0])] = str(info[project.index(x[0])]) + "\n" + x[1]

    except daily.DoesNotExist:
        return HttpResponse(-1)
    return JsonResponse({"project": project, "info": info}, safe=False)


# 10.10.152.66/api/weekly
@csrf_exempt
def save_weekly(request):
    """
    组员保存各自周报信息
    :param request:
    :return:
    """
    user = request.POST['user']
    team = request.POST['team']
    data = json.loads(request.POST['data'])
    action = request.POST['action']
    weekly = TeamUtils.get_team_weekly(team)
    if action == "insert":
        try:
            for i in range(len(data['project'])):
                weekly_info = weekly()
                weekly_info.project = data['project'][i]
                weekly_info.info = data['info'][i]
                weekly_info.time = data['time'][i]
                weekly_info.next_week = data['next_week'][i]
                weekly_info.difficult = data['difficult'][i]
                weekly_info.date = datetime.datetime.now().strftime("%Y-%m-%d")
                weekly_info.email = user
                weekly_info.save()
        except weekly.DoesNotExist:
            return HttpResponse(-1)
    else:
        try:
            for i in range(len(data['id'])):
                weekly.objects.filter(id=data['id'][i]).update(
                    project=data['project'][i],
                    info=data['info'][i],
                    time=data['time'][i],
                    next_week=data['next'][i],
                    difficult=data['difficult'][i]
                )
        except weekly.DoesNotExist:
            return HttpResponse(-1)
    return HttpResponse(0)


def statistics_weekly(request):
    return render(request, 'report/collect_weekly.html')


# 10.10.152.66/api/weekly/team
def collect_weekly(request):
    """
    获取指定部门所有成员的周报，进行汇总
    :param request:
    :return:
    """
    team = request.GET['team']
    try:
        weekly = TeamUtils.get_team_weekly(team)
        today_all = weekly.objects.filter(date__week=datetime.datetime.now().isocalendar()[1]).filter(total=False)
        if today_all.exists() is False:
            return HttpResponse(0)
        current_user = [x['email'] for x in today_all.values('email').distinct()]
        team_user = [x.email for x in User.objects.filter(team__name=team)]
        ret_list = []
        for x in list(set(current_user) ^ set(team_user)):
            ret_list.append(User.objects.get(email=x).name)

        total = today_all.values_list("project", "info", "time", "next_week", "difficult")
        project = list(set([x[0] for x in total]))
        result = [{"project": x, "info": "", "time": 0.0, "next_week": "", "difficult": ""} for x in project]

        for x in total:
            for y in result:
                if x[0] == y['project']:
                    if x[1] != "" and x[1] is not None:
                        y['info'] += (x[1] + "\n")
                    elif x[1] == "":
                        y['info'] = ""
                    if x[2] != "":
                        y['time'] += float(x[2])
                    if x[3] != "" and x[3] is not None:
                        y['next_week'] += (x[3] + "\n")
                    elif x[3] == "":
                        y['next_week'] = ""
                    if x[4] != "" and x[4] is not None:
                        y['difficult'] += (x[4] + "\n")
                    elif x[4] == "":
                        y['difficult'] = ""

    except weekly.DoesNotExist:
        return HttpResponse(-1)
    return JsonResponse({'data': result,
                         'name': ret_list, 'num': (len(team_user) - len(ret_list))}, safe=False)


# 10.10.152.66/api/weekly/formal
@csrf_exempt
def save_weekly_total(request):
    user = request.POST['user']
    team = request.POST['team']
    if request.POST['data'] != "":
        data = json.loads(request.POST['data'])
    action = request.POST['action']
    weekly = TeamUtils.get_team_weekly(team)
    try:
        if action == "insert":
            for x in data:
                weekly_new = weekly()
                weekly_new.project = x['project']
                weekly_new.info = x['info']
                weekly_new.time = x['time']
                weekly_new.next_week = x['next_week']
                weekly_new.difficult = x['difficult']
                weekly_new.email = user
                weekly_new.date = datetime.datetime.now().strftime("%Y-%m-%d")
                weekly_new.total = True
                weekly_new.save()
        elif action == 'modify':
            for y in data:
                weekly.objects.filter(id=y['id']).update(
                    project=y['project'],
                    info=y['info'],
                    time=y['time'],
                    next_week=y['next_week'],
                    difficult=y['difficult']
                )
        elif action == 'reset':
            weekly.objects.filter(date__week=datetime.datetime.now().isocalendar()[1]).filter(total=True).delete()
    except weekly.DoesNotExist:
        return HttpResponse(-1)

    return HttpResponse(0)


# 10.10.152.66/api/weekly/formal
def get_weekly_official(request):
    """
    获取指定部门的正式周报
    :param request:
    :return:
    """
    team = request.GET['team']
    weekly = TeamUtils.get_team_weekly(team)

    try:
        result = weekly.objects.filter(date__week=datetime.datetime.now().isocalendar()[1]).filter(total=True)
        if result.exists() is False:
            return HttpResponse(0)
    except weekly.DoesNotExist:
        return HttpResponse(-1)
    return JsonResponse(list(result.values()), safe=False)


@csrf_exempt
def download_weekly(request):
    excel = Excel()
    team = request.POST["team"]
    data = json.loads(request.POST["data"])
    return excel.write_weekly_to_excel(data, team)


# 10.10.152.66/api/search/weekly
def search_weekly(request):
    search_type = request.GET['type']
    date = request.GET['date']
    person = request.GET['person']
    team = request.GET['search_team']

    weekly = TeamUtils.get_team_weekly(team)

    try:
        if int(search_type) == 0:
            result = weekly.objects.filter(
                date__week=datetime.datetime.strptime(date, "%Y-%m-%d").isocalendar()[1]).filter(email=person).filter(
                total=False)
        elif int(search_type) == 1:
            result = weekly.objects.filter(
                date__week=datetime.datetime.strptime(date, "%Y-%m-%d").isocalendar()[1]).filter(total=True)
        if result.exists() is False:
            return HttpResponse(0)

    except weekly.DoesNotExist:
        return HttpResponse(-1)

    return JsonResponse(list(result.values()), safe=False)


# 10.10.152.66/api/daily/team
def get_daily_total(request):
    user = request.GET['user']
    team = request.GET['team']
    date = request.GET['date']
    daily = TeamUtils.get_team_daily(team)
    data = {}
    for x in daily:
        info = x.objects.filter(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        data[str(x.__name__)] = list(info.values())

    return JsonResponse(data, safe=False)


def manage_weekly(request):
    return render(request, 'report/manage_weekly.html')


# 10.10.152.66/api/weekly/formal/team
def get_weekly_total(request):
    team = request.GET['team']
    date = request.GET['date']
    weekly = TeamUtils.get_team_weekly(team)
    data = {}
    for x in weekly:
        info = x.objects.filter(date__week=datetime.datetime.strptime(date, "%Y-%m-%d").date().isocalendar()[1]).filter(
            total=True)
        data[str(x.__name__)] = list(info.values())
    return JsonResponse(data, safe=False)


def svn_up(request):
    """
    临时占用，hipad wiki svn文档库更新
    :param request:
    :return:
    """
    client = svn.local.LocalClient("/home/daiqingchen/project/wiki/")
    try:
        client.update()
    except svn.exception.SvnException:
        return HttpResponse(-1)
    return HttpResponse(0)


@csrf_exempt
def hour_allocation(request):
    """
    统计所有员工在某月的项目工时分配
    :param request:
    :return:
    """
    date = request.POST['date']
    per_total_hour = request.POST['hour']
    user = User.objects.all().iterator()
    projects = Project.objects.all()
    result = []
    result.append([x.name for x in projects])
    result[0].insert(0, "")
    result[0].remove("团队建设")
    i = 0

    for x in user:
        if x.team.name != 'director':
            i += 1
            temp = [0 for _ in range(projects.count())]
            temp[0] = x.name
            result.append(temp)
            weekly = TeamUtils.get_team_weekly(x.team.name)
            weekly_result = weekly.objects.filter(email=x.email).filter(date__month=4).filter(total=False).values("project", "time")
            for y in weekly_result:
                if y['project'] in result[0]:
                    index = result[0].index(y['project']) + 1
                    result[i][index] += float(y['time']) / float(per_total_hour)
                    result[i][index] = float('%.2f' % result[i][index])
            result[i].append(float('%.2f' % sum(result[i][1:])))
    excel = Excel()
    return excel.write_hour_allocation_to_excel(result)