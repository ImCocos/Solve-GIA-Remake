from django.contrib import admin

from .models import *


class VariantAdmin(admin.ModelAdmin):
    pass


class TaskAdmin(admin.ModelAdmin):
    pass


admin.site.register(Variant, VariantAdmin)
admin.site.register(Task, TaskAdmin)
