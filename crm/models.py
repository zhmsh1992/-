from django.db import models
from django.utils.safestring import mark_safe
from rbac.models import User



source_type = (('qq', "qq群"),
               ('baidu_ads', "百度推广"),
               ('office_direct', "直接上门"),
               ('WoM', "口碑"),
               ('others', "其它"),)







class Department(models.Model):
    """
    部门表
    """
    name = models.CharField(max_length=32, verbose_name="部门名称")
    count = models.IntegerField(verbose_name="人数", default=0)


class UserProfile(User,models.Model):
    """
    用户表
    """
    username = models.EmailField(max_length=255, unique=True, )
    password = models.CharField(max_length=128, verbose_name='密码')
    name = models.CharField('名字', max_length=32)
    department = models.ForeignKey('Department', default=None, blank=True, null=True)
    mobile = models.CharField('手机', max_length=32, default=None, blank=True, null=True)
    memo = models.TextField('备注', blank=True, null=True, default=None)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    """
    客户表
    """

    name = models.CharField('姓名', max_length=32, blank=True, null=True,)
    sex_type = (('male', '男'), ('female', '女'))
    sex = models.CharField("性别", choices=sex_type, max_length=16, default='male', blank=True, null=True)
    phone = models.BigIntegerField('手机号', blank=True, null=True)
    source = models.CharField('客户来源', max_length=64, choices=source_type, default='qq')
    customer_note = models.TextField("客户备注", blank=True, null=True, )
    date = models.DateTimeField("咨询日期", auto_now_add=True)
    last_consult_date = models.DateField("最后跟进日期", auto_now_add=True)
    next_date = models.DateField("预计再次跟进时间", blank=True, null=True)
    network_consultant = models.ForeignKey('UserProfile', blank=True, null=True, verbose_name='咨询师',
                                           related_name='network_consultant')
    consultant = models.ForeignKey('UserProfile', verbose_name="销售", related_name='customers', blank=True, null=True, )

    def __str__(self):
        return "{}".format( self.name)



class ConsultRecord(models.Model):
    """
    跟进记录表
    """
    customer = models.ForeignKey('Customer', verbose_name="所咨询客户")
    note = models.TextField(verbose_name="跟进内容...")
    status = models.CharField("跟进状态", max_length=8,  help_text="选择客户此时的状态")
    consultant = models.ForeignKey("UserProfile", verbose_name="跟进人", related_name='records')
    date = models.DateTimeField("跟进日期", auto_now_add=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)




class PaymentRecord(models.Model):
    """
    缴费记录表
    """
    pay_type = models.CharField("费用类型",  max_length=64, default="deposit")
    paid_fee = models.IntegerField("费用数额", default=0)
    note = models.TextField("备注", blank=True, null=True)
    date = models.DateTimeField("交款日期", auto_now_add=True)
    customer = models.ForeignKey('Customer', verbose_name="客户")
    consultant = models.ForeignKey('UserProfile', verbose_name="销售")
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)

    status_choices = (
        (1, '未审核'),
        (2, '已审核'),
    )
    status = models.IntegerField(verbose_name='审核', default=1, choices=status_choices)

    confirm_date = models.DateTimeField(verbose_name="确认日期", null=True, blank=True)
    confirm_user = models.ForeignKey(verbose_name="确认人", to='UserProfile', related_name='confirms', null=True,
                                     blank=True)


