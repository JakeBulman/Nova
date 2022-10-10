from django.contrib import admin

from .models import Centres


class CentresAdmin(admin.ModelAdmin):
    list_display = ['Centre_name', 'Centre_ID']
    search_fields = ['Centre_name']


admin.site.register(Centres, CentresAdmin)