from django.shortcuts import render, redirect, HttpResponse, reverse
from crm import models
from crm.forms import CustomerForm
from django.http.request import QueryDict
from crm.utils.pagination import Pagination
from crm.utils.urls import reverse_url
from django.db import transaction

# def customer_list(request):
#     if request.path_info == reverse('customer_list'):
#         all_customer = models.Customer.objects.filter(consultant__isnull=True)
#     else:
#         all_customer = models.Customer.objects.filter(consultant=request.user_obj)
#
#     return render(request, 'customer_list.html', {'all_customer': all_customer})

from django.views import View
from django.db.models import Q
from django.conf import settings, global_settings


class CustomerList(View):

    def get(self, request):
        # query = request.GET.get('query', '')
        # 'django.http.request.QueryDict'
        # dic = request.GET
        # dic._mutable = True
        # dic['page'] = 1
        # print(dic)

        q = self.search(['qq', 'name', ])

        if request.path_info == reverse('customer_list'):
            all_customer = models.Customer.objects.filter(q, consultant__isnull=True, )
        else:
            all_customer = models.Customer.objects.filter(q, consultant=request.user_obj)

        page = Pagination(request.GET.get('page'), all_customer.count(), request.GET.copy(), 10)
        return render(request, 'consultant/customer_list.html',
                      {'all_customer': all_customer[page.start:page.end], 'page_html': page.page_html}, )

    def post(self, request):

        action = request.POST.get('action')

        if not hasattr(self, action):
            return HttpResponse('非法操作')

        ret = getattr(self, action)()
        if ret:
            return ret

        return self.get(request)

    def multi_apply(self):
        # 公户变私户
        ids = self.request.POST.getlist('ids')
        # 方式一
        # models.Customer.objects.filter(pk__in=ids).update(consultant=self.request.user_obj)

        # 当前销售私户的数量   +  申请的客户的数量   > 上限
        if self.request.user_obj.customers.all().count() + len(ids) > settings.MAX_CUSTOMER_NUM:
            return HttpResponse('做人不要太贪心了，给别人留点')

        # 开启事务：
        with transaction.atomic():
            queryset = models.Customer.objects.filter(pk__in=ids, consultant__isnull=True).select_for_update()  # 加行锁
            # 跟新
            # 判断提交的数据数  和 查询的数据数
            if len(ids) == queryset.count():
                queryset.update(consultant=self.request.user_obj)
                return
            return HttpResponse('你的手速太慢，已经别别人掳走了')

        # 方式二
        # self.request.user_obj.customers.add(*models.Customer.objects.filter(pk__in=ids))

    def multi_pub(self):
        # 私户变公户
        ids = self.request.POST.getlist('ids')
        # 方式一
        # models.Customer.objects.filter(pk__in=ids).update(consultant=None)

        # 方式二
        self.request.user_obj.customers.remove(*models.Customer.objects.filter(pk__in=ids))

    def search(self, filed_list):
        query = self.request.GET.get('query', '')
        # q = Q(Q(qq__contains=query) | Q(name__contains=query))
        q = Q()
        q.connector = 'OR'
        for field in filed_list:
            # q.children.append(Q(qq__contains=query))
            q.children.append(Q(('{}__contains'.format(field), query)))
        return q


def add_customer(request):
    # 创建一个没有数据的Form
    form_obj = CustomerForm()

    if request.method == 'POST':
        # 创建一个包含提交数据的Form
        form_obj = CustomerForm(request.POST)
        # 对数据进行校验
        if form_obj.is_valid():
            form_obj.save()  # 新增

            return redirect(reverse_url(request, 'customer_list'))

    return render(request, 'consultant/add_customer.html', {'form_obj': form_obj})


def edit_customer(request, edit_id):
    obj = models.Customer.objects.filter(pk=edit_id).first()

    form_obj = CustomerForm(instance=obj)

    if request.method == 'POST':
        # 有修改的数据和原始的数据
        form_obj = CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()

            return redirect(reverse_url(request, 'customer_list'))

    return render(request, 'consultant/edit_customer.html', {'form_obj': form_obj})


# 新增和编辑客户
def customer_change(request, edit_id=None):
    obj = models.Customer.objects.filter(pk=edit_id).first()
    form_obj = CustomerForm(instance=obj)

    title = '编辑客户' if edit_id else '新增客户'
    if request.method == 'POST':
        # 有修改的数据和原始的数据
        form_obj = CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()

            return redirect(reverse('customer_list'))

    return render(request, 'consultant/customer_change.html', {'form_obj': form_obj, 'title': title})
