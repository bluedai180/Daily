from django.shortcuts import render

from .models import User, Team, AppDaily
from .excel import Excel
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import datetime
import json

list_info_today = []
list_info_result = []


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
        if info.team.name == "app":
            today = AppDaily.objects.filter(date=timezone.now().date()).filter(email=user)
            past = AppDaily.objects.filter(email=user).filter(
                date__range=(date - datetime.timedelta(days=3), date - datetime.timedelta(days=1)))
            if today.count() == 0:
                user_info['today'] = ""
            else:
                user_info['today'] = list(today.values())
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

        if len_insert != 0:
            for x in data['insert']:
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
                user_team.email = user.email
                user_team.save()

        if len_del != 0:
            for x in data['del']:
                AppDaily.objects.get(id=x).delete()

        if len_modify != 0:
            for i in range(len_modify):
                AppDaily.objects.filter(id=data['modify']['id'][i]).update(
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
    except AppDaily.DoesNotExist:
        return HttpResponse(-1)

    return HttpResponse(0)


def statistics(request):
    return render(request, 'report/collect.html')


def collect(request):
    team = request.GET['team']
    list_info_today.clear()
    try:
        if team == "app":
            daily = AppDaily.objects.filter(date=timezone.now().date())
            if daily.count() == 0:
                return HttpResponse(0)
            current_user = [x['email'] for x in daily.values('email').distinct()]
            team_user = [x.email for x in User.objects.filter(team__name='app')]
            ret_list = []
            for x in list(set(current_user) ^ set(team_user)):
                ret_list.append(User.objects.get(email=x).name)
            for x in daily.values_list():
                list_info_today.append(list(x)[1:-1])
    except AppDaily.DoesNotExist:
        return HttpResponse(-1)
    info = {'info': list(daily.values()), 'name': ret_list}
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


def search_info(request):
    list_info_result.clear()
    info = json.loads(request.GET['info'])
    if info['team'] == "app":
        worktype = info['worktype']
        bugid = info['bugid']
        describe = info['describe']
        solution = info['solution']
        start_date = info['start_date']
        end_date = info['end_date']
        user = info['user']
        result = AppDaily.objects.filter(work_type=worktype)
        if bugid != "":
            result = result.filter(bugid=bugid)
        elif describe != "":
            result = result.filter(describe=describe)
        elif solution != "":
            result = result.filter(solution=solution)
        elif start_date != "" and end_date != "":
            result = result.filter(date__range=(start_date, end_date))
        elif user != "":
            result = result.filter(email=user)

    for x in result.values_list():
        list_info_result.append(list(x)[1:-1])

    if result.count() == 0:
        return HttpResponse(0)
    return JsonResponse(list(result.values()), safe=False)


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
