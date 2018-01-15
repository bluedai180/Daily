from django.contrib import admin

from .models import Team, User, AppDaily, FrameworkDaily, DriverDaily, ProtocolDaily


class UserAdmin(admin.ModelAdmin):
    # fields = ["name", "email", "team"]
    list_display = ("name", "email", "team", "permission")


class DailyAdmin(admin.ModelAdmin):
    list_display = ("describe", "person", "date")


admin.site.register(Team)
admin.site.register(User, UserAdmin)
admin.site.register(AppDaily, DailyAdmin)
admin.site.register(FrameworkDaily, DailyAdmin)
admin.site.register(DriverDaily, DailyAdmin)
admin.site.register(ProtocolDaily, DailyAdmin)
