from django.utils.translation import ugettext_lazy as _
from django.db import models
from wechat_member.models import Member

class Qrcode(models.Model):
    """
    Qrcode Model base on django wechat member
    """
    member = models.OneToOneField(Member, related_name='qrcode',\
            verbose_name=_('member'))
    ticket = models.CharField(_('ticket'), max_length=200)
    inviter = models.ForeignKey('self', related_name='people',\
            blank=True, null=True, verbose_name=_('inviter'))
    created = models.DateTimeField(_('created'), auto_now_add=True)

    def __unicode__(self):
        return self.member.name

    def qrcode_url(self):
        return 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s'\
                % self.ticket

    def invite_count(self):
        return self.inviter.count()

    class Meta(object):
        verbose_name = _('qrcode')
        verbose_name_plural = _('qrcode')

    qrcode_url.short_description = _('qrcode url')
    invite_count.short_description = _('invite count')
