from django.shortcuts import render, redirect, HttpResponse, reverse
from crm import models
from crm.forms import RegForm
import hashlib
from django.views.decorators.csrf import ensure_csrf_cookie
from rbac.service.permission import init_permission

def index(request):
    return HttpResponse('index')

# @ensure_csrf_cookie
def login(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        pwd = request.POST.get('password')

        md5 = hashlib.md5()
        md5.update(pwd.encode('utf-8'))
        pwd = md5.hexdigest()

        obj = models.UserProfile.objects.filter(username=user, password=pwd, is_active=True).first()
        if obj:
            request.session['pk'] = obj.pk
            init_permission(request,obj)
            return redirect(reverse('customer_list'))

    return render(request, 'login.html')

def reg(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            # 插入到数据库
            # print(form_obj.cleaned_data)
            # form_obj.cleaned_data.pop('re_pwd')
            # models.UserProfile.objects.create(**form_obj.cleaned_data)
            form_obj.save()
            return redirect(reverse('login'))

    return render(request, 'reg.html', {'form_obj': form_obj})
