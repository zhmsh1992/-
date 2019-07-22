# from django.contrib.auth.middleware import AuthenticationMiddleware

from django.utils.deprecation import MiddlewareMixin
from crm import models
from django.shortcuts import redirect, reverse


class AuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 拿到id 获取到对象

        if request.path_info in [reverse('login'), reverse('reg')] or request.path_info.startswith('/admin/'):
            return

        pk = request.session.get('pk')
        obj = models.UserProfile.objects.filter(pk=pk).first()
        if obj:
            request.user_obj = obj
            return
        return redirect(reverse('login'))
