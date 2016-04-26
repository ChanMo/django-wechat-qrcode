#!/usr/bin/python
# vim: set fileencoding=utf8 :
from django.db import models
from wechat_member.models import Member as Member

class Qrcode(models.Model):
    member = models.OneToOneField(Member, related_name='qrcode', verbose_name='二维码')
    ticket = models.CharField(max_length=200, verbose_name='票据')
    inviter = models.ForeignKey('self', related_name='people', blank=True, null=True, verbose_name='邀请人')
    created = models.DateTimeField(auto_now_add=True, verbose_name='created', verbose_name='创建时间')
    def __unicode__(self):
        return self.member.name

    def qrcode_url(self):
        return 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s' % self.ticket

    def people_count(self):
        return self.people.count()

    class Meta(object):
        verbose_name = 'qrcode'
        verbose_name_plural = 'qrcode'
