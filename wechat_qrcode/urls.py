from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^wx/$', views.index, name='wx'),
    url(r'^$', views.Qrcode.as_view(), name='qrcode'),
]
