#encoding: utf-8
from login.models import LoginUser, GoodsissueGoods, GoodsissueIssuer, GoodsissueSaler
from dtiaozao import function as fun


#用户注册处理
def user_register(date):
    condition = fun.warp_data(date)
    # print(condition)
    if condition['passwd'] != condition['repasswd']:
        return 0
    del condition['repasswd']
    passwd = fun.mk_md5(condition['passwd'])
    condition['passwd'] = passwd
    #数据库的存储
    u = LoginUser(**condition)
    u.save()
    if u.name:
        return 1
    else:
        return -1

#用户登录处理
def user_login(date):
    condition = fun.warp_data(date)
    email = condition['email']
    passwd = fun.mk_md5(condition['passwd'])
    r = LoginUser.objects.get(email=email)
    #判断数据库的账号匹配结果是否存在以及密码是否匹配
    if not r or passwd != r.passwd:
        r = {}
    return r