from django.conf.urls import url
import views
urlpatterns=[
    url(r'^$',views.index),
    # url(r'^list/$',views.list),
    # url(r'^detail/$',views.detail),
    url(r'list(\d+)_(\d+)_(\d+)/$',views.list),
    url('^(\d+)/$',views.detail),
    url('^search/$',views.MySearchView()),
]













