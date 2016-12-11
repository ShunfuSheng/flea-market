#encoding: utf-8
from login.models import LoginUser, GoodsissueGoods, GoodsissueIssuer, GoodsissueSaler
from dtiaozao import function as fun

#得到全部商品信息模块处理
def get_goods_info():
    u = GoodsissueGoods.objects.all()
    return u


#得到单条商品信息模块处理
def get_goods_detail(data):
    condition = fun.warp_data(data)
    id = condition.get('id')
    u = GoodsissueGoods.objects.get(id=id)
    if u:
        return u
    else:
        return {}


#点击购买模块处理
def purchase(data, buyer_id):
    condition = fun.warp_data(data)
    tradeDate = fun.now()
    condition['buyer_id'] = buyer_id
    u = GoodsissueSaler(**condition)
    u.tradedate = tradeDate
    u.save()
    if u:
        return 1
    else:
        return -1


#购买和售出记录模块处理
def trade_his(uid):
    result = []
    info = {}
    for buyer_id in uid:
        #判断是购买功能还是售出功能传入的参数
        if buyer_id[1]:
            u = GoodsissueSaler.objects.filter(buyer_id=buyer_id[0], goods_id=buyer_id[1])
        else:
            u = GoodsissueSaler.objects.filter(buyer_id=buyer_id[0])
        #购买与售出的公共模块
        if u:
            for re in u:
                info['goods_id'] = re.goods_id
                info['buyer_id'] = buyer_id[0]
                info['tradedate'] = re.tradedate
                p = GoodsissueGoods.objects.get(id=re.goods_id)
                info['goods_name'] = p.name
                info['goods_price'] = p.price
                result.append(info)
                info = {}
        else:
            return []
    #对结果集进行排序，以销售日期的先后做排序
    result.sort(lambda x,y: cmp(x['tradedate'],y['tradedate']), reverse=True)
    return result
