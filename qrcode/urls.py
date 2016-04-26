from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.QrcodeView.as_view(), name='qrcode'),
    url(r'^api/$', views.index, name='api'),
]
