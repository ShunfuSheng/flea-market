#encoding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
import controller
from trade.controller import trade_his
from login.models import GoodsissueGoods, GoodsissueSaler
from dtiaozao import function as fun


#商品发布模块
def issue(req):
    if not req.session.get('islogin'):
        msg = '你还未登陆，请先登陆！'
        return render_to_response('error_msg.html', locals())
    if req.method == 'GET':
        uid = req.session['user_info']['uid']
        #获取商品信息
        rt = controller.get_goods(uid)
        return render_to_response('user_issue.html', locals(), context_instance=RequestContext(req))
    else:
        #获取form表单的基本信息
        data = req.POST
        #获取发布者ID
        uid = req.session['user_info']['uid']

        #将额外信息存入字典中
        extends = {}
        extends['uid'] = uid
        extends['imgName'] = False

        #获取form表单的图片信息
        imgfile = req.FILES.get('imagefile', None)

        #上传图片
        if imgfile:
            imgName = imgfile.name
            extends['imgName'] = imgName
            if not fun.handle_uploaded_file(imgfile):
                msg = '文件上传失败，请联系管理员！！'
                return render_to_response('error_msg.html', locals(), context_instance=RequestContext(req))

        #数据库的存储和更新操作
        rt = controller.store_goods(data, extends)
        # print rt
        if rt == 1 or rt == 2:
            return HttpResponseRedirect('/goodsIssue/issue')
        elif rt == -1:
            msg = '数据库的更新操作失败，请联系管理员！'
            return render_to_response('error_msg.html', locals(), context_instance=RequestContext(req))
        else:
            msg = '数据库的新增操作失败，请联系管理员！'
            return render_to_response('error_msg.html', locals(), context_instance=RequestContext(req))



#商品下架模块
def delGoods(req):
    data = req.GET
    isDel = controller.del_goods(data)
    if isDel == -1:
        msg = '删除商品失败，请联系管理员！'
        return render_to_response('error_msg.html', locals(), context_instance=RequestContext(req))
    else:
        uid = req.session['user_info']['uid']
        rt = controller.get_goods(uid)
        return render_to_response('user_issue.html', locals(), context_instance=RequestContext(req))



#销售记录模块
def saleHis(req):
    if not req.session.get('islogin'):
        msg = '你还未登陆，请先登陆！'
        return render_to_response('error_msg.html', locals())
    if req.method == 'GET':
        uid = req.session['user_info']['uid']

        #从商品表中获取商品id，然后到售出表中获取到购买者的id
        p = GoodsissueGoods.objects.filter(owner_id=uid)
        if not p:
            msg = '你还未上架任何商品！'
            return render_to_response('error_msg.html', locals(), context_instance=RequestContext(req))

        #定义一个购买者id的列表
        buyer_id = []

        #遍历卖家所有的商品id，购买者id和商品id为一对多的关系
        for goods in p:
            goods_id = goods.id
            p2 = GoodsissueSaler.objects.filter(goods_id=goods_id)
            if p2:
                #因为二级list无法作为迭代器，因此使用元组
                buyer_id.append((p2[0].buyer_id, goods_id))
            else:
                buyer_id.append((0, 0))

        #对list中的数据进行去重工作
        buyer_id = list(set(buyer_id))
        #跨APP调用trade子模块中controller中的方法，传入一个列表对象
        result = trade_his(buyer_id)
        return render_to_response('sale_history.html', locals(), context_instance=RequestContext(req))


#售出消息接收模块
def message(req):
    return 1

