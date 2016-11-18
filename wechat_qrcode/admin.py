from django.contrib import admin
from .models import Qrcode as QrcodeModel

class Qrcode(admin.ModelAdmin):
    list_display = ('member', 'invite_count', 'inviter', 'created')
    list_filter = ('created',)
    list_per_page = 12

admin.site.register(QrcodeModel, Qrcode)
