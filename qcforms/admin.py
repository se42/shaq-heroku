from django.contrib import admin

from . import models

admin.site.register(models.IntNCReport)
admin.site.register(models.IntNCImage)
admin.site.register(models.QualityAlert)
