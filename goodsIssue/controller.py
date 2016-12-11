#encoding: utf-8
from login.models import LoginUser, GoodsissueGoods, GoodsissueIssuer, GoodsissueSaler
from dtiaozao import function as fun


#从数据库中取得商品信息
def get_goods(uid):
    #扫描商品表
    owner_id = LoginUser.objects.get(id=uid)
    u = GoodsissueGoods.objects.filter(owner_id=owner_id)
    return u


#商品下架处理
def del_goods(data):
    goods_id = fun.warp_data(data)['id']
    p = GoodsissueGoods.objects.get(id=goods_id)
    if p:
        p.delete()
    else:
        return -1


#商品信息发布处理
def store_goods(data, extends):
    condition = fun.warp_data(data)
    issueDate = fun.now()
    #定义存储商品发布者信息的字典
    issuer = {}
    # issuer['issueDate'] = issueDate
    #存入商品发布者的ID
    owner_id = LoginUser.objects.get(id=extends['uid'])
    condition['owner_id'] = extends['uid']
    issuer['uid'] = owner_id
    #存入图片名
    if extends['imgName']:
        condition['imagefile'] = extends['imgName']
    #弹出id
    id = condition.pop('id')
    if id:
        #更新商品表操作，全更新，首先将值为空的字段弹出去
        for co in condition.keys():
            if not condition[co]:
                condition.pop(co)
        u1 = GoodsissueGoods.objects.filter(id=id).update(**condition)
        #更新商品发布者表操作，部分更新
        goodsId = GoodsissueGoods.objects.get(id=id)
        u2 = GoodsissueIssuer.objects.filter(goods_id=goodsId)
        u2.issueDate = issueDate
        if u1 or u2:
            return 1
        else:
            return -1
    else:
        #新增商品表操作
        u3 = GoodsissueGoods(**condition)
        u3.save()
        #新增商品发布者表操作
        goodsId = GoodsissueGoods.objects.get(owner_id=issuer['uid'], name=condition['name']).id
        issuer['goods_id'] = goodsId
        u4 = GoodsissueIssuer(**issuer)
        u4.issuedate = issueDate
        u4.save()
    if u3:
        return 2
    else:
        return -2


