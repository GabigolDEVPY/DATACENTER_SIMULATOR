from django.contrib import admin
from operation.models import IaInstallationTask

# Register your models here.
@admin.register(IaInstallationTask)
class IaInstallationTaskAdmin(admin.ModelAdmin):
    list_display = ('ai_instance', 'started_at', 'finished_at')