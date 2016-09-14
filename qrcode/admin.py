from django.contrib import admin
from .models import Qrcode

class QrcodeAdmin(admin.ModelAdmin):
    list_display = ('member', 'inviter', 'created')
    list_filter = ('created',)
    list_per_page = 12

admin.site.register(Qrcode, QrcodeAdmin)
