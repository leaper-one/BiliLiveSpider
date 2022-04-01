# -*- coding: utf-8 -*-

from django.http import HttpResponse

from model.models import naomi


# 数据库操作
def testdb(request):
    test1 = naomi(username='Cunky', file='god.wowsreplay', remark='god test', qn=1)
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")