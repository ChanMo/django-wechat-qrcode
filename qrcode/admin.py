from django.contrib import admin
from .models import Qrcode

class QrcodeAdmin(admin.ModelAdmin):
    list_display = ('member', 'inviter', 'people_count', 'created')
    list_filter = ('created',)
    list_per_page = 20

admin.site.register(Qrcode, QrcodeAdmin)
