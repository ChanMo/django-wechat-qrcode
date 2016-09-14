from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from wechat_member.views import WxMemberView
from wechat import api
from wechat_member.models import Member
from .models import Qrcode

class QrcodeApi(api.Base):
    """
    get qrcode model
    """
    def get_qrcode(self, member):
        try:
            qrcode = Qrcode.objects.get(member=member)
        except Qrcode.DoesNotExist:
            qrcode = self.create_qrcode(member)
        return qrcode


    """
    create member for django_wechat_member
    """
    def create_member(self, openid):
        token = self.get_token()
        url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (token, openid)
        data = self.get_data(url)
        member = Member(
            name = data['nickname'],
            avatar = data['headimgurl'],
            openid = openid,
            city = data['city'],
        )
        member.save()
        return member

    """
    create qrcode
    use qrcode.id for ticket key
    """
    def create_qrcode(self, member, inviter_id=False):
        if inviter_id:
            qrcode = Qrcode(
                member = member,
                inviter_id = inviter_id,
            )
        else:
            qrcode = Qrcode(
                member = member,
            )
        qrcode.save()
        wx_qr = api.Qrcode()
        qrcode.ticket = wx_qr.get_ticket(qrcode.id)
        qrcode.save()
        return qrcode


    """
    set qrcode inviter
    """
    def set_qr_inviter(self, openid, inviter_id):
        try:
            member = Member.objects.get(openid=openid)
        except Member.DoesNotExist:
            member = self.create_member(openid)
        try:
            qrcode = Qrcode.objects.get(member=member)
            if not qrcode.inviter:
                qrcode.inviter_id = inviter_id
                qrcode.save()
        except Qrcode.DoesNotExist:
            self.create_qrcode(member, inviter_id)



class QrcodeResponse(api.Response):
    'qrcode api extend wx api'

    def set_keyword(self):
        data = self.receive_data
        try:
            keyword = data['Content']
        except KeyError:
            try:
                if data['MsgType'] == u'event':
                    if data['Event'] == u'subscribe':
                        try:
                            if data['EventKey'][0:8] == u'qrscene_':
                                qrvalue = data['EventKey'][8:]
                                qrapi = QrcodeApi()
                                qrapi.set_qr_inviter(data['FromUserName'], qrvalue)
                        except KeyError:
                            pass
                        keyword = 'subscribe'
                    elif data['Event'] == u'CLICK':
                        keyword = data['EventKey']
                    elif data['Event'] == u'SCAN':
                        keyword = u'default'
                    else:
                        keyword = data['Event']
                else:
                    keyword = 'customer_service'
            except KeyError:
                keyword = 'customer_service'

        self.keyword = keyword



@csrf_exempt
def index(request):
     wx = api.Base()
     data = request.GET
     try:
         echostr = data['echostr']
         result = wx.check_sign(data)
         if result:
             return HttpResponse(echostr)
         else:
             return HttpResponse('error')
     except KeyError:
         wx_res = QrcodeResponse(request)
         result = wx_res.get_response()
         return HttpResponse(result)

class QrcodeView(WxMemberView, TemplateView):
    template_name = 'qrcode/qrcode.html'
    def get_context_data(self, **kwargs):
        context = super(QrcodeView, self).get_context_data(**kwargs)
        try:
            qrcode = Qrcode.objects.get(member=self.wx_member)
        except Qrcode.DoesNotExist:
            qrcodeapi = QrcodeApi()
            qrcode = qrcodeapi.create_qrcode(self.wx_member)
        context['qrcode'] = qrcode
        return context
