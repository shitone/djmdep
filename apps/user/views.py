from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from apps.user.models import User, Department
import json
import urllib

# Create your views here.


def index(request):
    return render(request, 'login.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password_md5 = request.POST['password']
        remember = request.POST['remember']
        user = User.objects.filter(username=username).first()
        if user is not None and user.verify_password(password_md5):
            auth.login(request, user)
            request.session.set_expiry(0)
            return HttpResponse(json.dumps(dict(succeed=True, ac=user.areacode)))
        return HttpResponse(json.dumps(dict(succeed = False)))
    return render(request, 'login.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        truename = request.POST['truename']
        department = request.POST['department']
        phone = request.POST['phone']
        user = User(username=username, password=password, truename=truename, department=department, phone=phone)
        user.save()
        return HttpResponse(json.dumps(dict(succeed=True)))


def iplogin(request):
    ip = request.META['REMOTE_ADDR']
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    f = urllib.request.urlopen(('http://10.116.32.81/aws_cimiss/index.php/Api/getFocusFromIp/?ip=' + ip))
    data = json.loads(f.read())
    areacode = data['code'][0:4] + '00'
    user = User.objects.filter(areacode=areacode).first()
    if user is not None:
        auth.login(request, user)
        request.session.set_expiry(0)
        return HttpResponse(json.dumps(dict(succeed=True, un=user.username, ac=user.areacode)))
    return HttpResponse(json.dumps(dict(succeed = False)))


@login_required()
def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


def department(request):
    departments = Department.objects.all()
    dpts = []
    for department in departments:
        dpt = {}
        dpt['id'] = department.id
        dpt['name'] = department.name
        dpts.append(dpt)
    return HttpResponse(json.dumps(dict(dpts = dpts)))