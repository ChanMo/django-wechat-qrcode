from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from .api import Qrcode as QrcodeApi, Message as MessageApi
from .models import Qrcode as QrcodeModel
from wechat_member.views import WxMemberView
from wechat_member.models import Member

@csrf_exempt
def index(request):
    wx = MessageApi()
    try:
        echostr = request.GET['echostr']
        return HttpResponse(echostr)
    except KeyError:
        """ Normal message """
        data = wx.receive(request.body)
        keyword = wx.get_keyword(data)
        result = wx.response(keyword, data)
        return HttpResponse(result)


class Qrcode(WxMemberView, TemplateView):
    template_name = 'wechat_qrcode/qrcode.html'
    def get_context_data(self, **kwargs):
        context = super(Qrcode, self).get_context_data(**kwargs)
        try:
            qrcode = QrcodeModel.objects.get(member=self.wx_member)
        except QrcodeModel.DoesNotExist:
            qrcodeapi = QrcodeApi()
            qrcode = qrcodeapi.create_qrcode(self.wx_member)
        context['qrcode'] = qrcode
        return context
