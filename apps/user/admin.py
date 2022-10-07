import copy
from django.contrib import admin

from apps.user.models import Activity, CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    class Meta:
        fields = '__all__'
        readonly_fields = ["last_activity", "views"]


admin.site.register(Activity)
