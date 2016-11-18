from django.test import TestCase
from .api import Qrcode as QrcodeApi, Message as MessageApi
from .models import Qrcode as QrcodeModel
from wechat_member.models import Member as MemberModel

class Qrcode(TestCase):
    def setUp(self):
        print("create data start...")
        self.member = MemberModel.objects.create(
            name='test',
            avatar='',
            openid='',
            city=''
        )
        print("create member success")

    def test_get_qrcode(self):
        api = QrcodeApi()
        result = api.get_qrcode(self.member)
        print(result)
