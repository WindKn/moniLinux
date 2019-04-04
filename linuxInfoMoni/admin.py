from django.contrib import admin

# Register your models here.

from linuxInfoMoni import models
admin.site.register(models.serverInfo)
admin.site.register(models.trace_detail)
admin.site.register(models.trace_info)