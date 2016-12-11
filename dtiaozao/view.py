#encoding: utf-8
__author__ = 'hadoop'

from django.shortcuts import render_to_response
from django.template import RequestContext
from login.models import LoginUser, GoodsissueGoods, GoodsissueIssuer, GoodsissueSaler
from dtiaozao import function as fun

#主页
def index(req):
    #获得数据库中的数据，全表扫描
    users = LoginUser.objects.all()
    goodses = GoodsissueGoods.objects.all()
    issuers = GoodsissueIssuer.objects.all()
    salers = GoodsissueSaler.objects.all()
    return render_to_response('index.html', locals(), context_instance=RequestContext(req))


#搜索引擎模块
def search(req):
    if req.method == 'GET':
        msg = '非法访问！！！'
        return render_to_response('error_msg.html', locals())
    data = fun.warp_data(req.POST)
    goods_name = data['keywords']
    goods_info = GoodsissueGoods.objects.filter(name__contains=goods_name)
    return render_to_response('goods_list.html', locals(), context_instance=RequestContext(req))
