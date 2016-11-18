import json
from wechat.api import Base
from wechat_message.api import Message as MessageApi
from wechat_member.models import Member
from .models import Qrcode as QrcodeModel

class Qrcode(Base):
    """
    get qrcode model
    """
    def get_qrcode(self, member):
        """ get qrcode object """
        try:
            qrcode = QrcodeModel.objects.get(member=member)
        except QrcodeModel.DoesNotExist:
            qrcode = self.create_qrcode(member)
        return qrcode

    def create_qrcode(self, member, inviter_id=None):
        """ create qrcode object """
        qrcode = QrcodeModel(member=member, inviter_id=inviter_id)
        qrcode.save()
        qrcode.ticket = self.get_ticket(qrcode.id)
        qrcode.save()
        return qrcode

    def get_ticket(self, id):
        """ create ticket from wechat """
        token = self.get_token()
        url = self.get_url('qrcode/create', {'access_token':token})
        data = {
            'action_name': 'QR_LIMIT_SCENE',
            'action_info': {
                'scene': {
                    'scene_id': id,
                }
            }
        }
        data = json.dumps(data)
        result = self.get_data(url, data)
        return result['ticket']

    def set_qr_inviter(self, openid, inviter_id):
        """ set inviter of qrcode object """
        try:
            member = Member.objects.get(openid=openid)
        except Member.DoesNotExist:
            member = self.create_member(openid)
        try:
            qrcode = QrcodeModel.objects.get(member=member)
            if not qrcode.inviter:
                qrcode.inviter_id = inviter_id
                qrcode.save()
        except QrcodeModel.DoesNotExist:
            self.create_qrcode(member, inviter_id)

    def create_member(self, openid):
        """ create member when subscribe by openid """
        token = self.get_token()
        url = 'https://api.weixin.qq.com/cgi-bin/user/info\
	?access_token=%s&openid=%s&lang=zh_CN' % (token, openid)
        data = self.get_data(url)
        member = Member(
            name = data['nickname'],
            avatar = data['headimgurl'],
            openid = openid,
            city = data['city'],
        )
        member.save()
        return member



class Message(MessageApi):
    """
    Extends MessageApi, add qrcode
    """
    def get_keyword(self, data):
        try:
            msg_type = data['MsgType']

            if msg_type == 'text':
                keyword = data['Content']
            elif msg_type == 'event':
                event = data['Event']
                if event == 'subscribe':
                    keyword = 'subscribe'
                    """ use qrcode """
                    try:
                        if data['EventKey'][0:8] == 'qrscene_':
                            qrvalue = data['EventKey'][8:]
                            qrcode = Qrcode()
                            qrcode.set_qr_inviter(data['FromUserName'], qrvalue)
                    except KeyError:
                        pass
                elif event == 'unsubscribe':
                    keyword = 'unsubscribe'
                elif event == 'CLICK':
                    keyword = data['EventKey']
                else:
                    keyword = 'default'
            else:
                keyword = 'default'

        except KeyError:
            keyword = 'default'

        return keyword
