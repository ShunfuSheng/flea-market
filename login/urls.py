from django.conf.urls import patterns, include, url

urlpatterns = patterns('login.views',
    url(r'^login', 'login'),
    url(r'^logout', 'logout'),
    url(r'^register', 'register'),
)