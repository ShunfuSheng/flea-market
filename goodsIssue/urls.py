from django.conf.urls import patterns, include, url

urlpatterns = patterns('goodsIssue.views',
        url(r'^issue', 'issue'),
        url(r'^delGoods', 'delGoods'),
        url(r'^saleHis', 'saleHis'),
        url(r'message', 'message'),
)
