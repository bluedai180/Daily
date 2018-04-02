from django.contrib import admin

from .models import Team, User, AppDaily, FrameworkDaily, DriverDaily, ProtocolDaily, Project, \
    AppWeekly, FrameworkWeekly, DriverWeekly, ProtocolWeekly, SPMDaily, SPMWeekly, App3Daily, App3Weekly


class UserAdmin(admin.ModelAdmin):
    # fields = ["name", "email", "team"]
    list_display = ("name", "email", "team", "permission")


class DailyAdmin(admin.ModelAdmin):
    list_display = ("person", "project", "describe", "date")


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', "app", "app3", "framework", "driver", "protocol", "spm")


class WeeklyAdmin(admin.ModelAdmin):
    list_display = ('project', 'email', 'date')


admin.site.register(Team)
admin.site.register(Project, ProjectAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(AppDaily, DailyAdmin)
admin.site.register(FrameworkDaily, DailyAdmin)
admin.site.register(DriverDaily, DailyAdmin)
admin.site.register(ProtocolDaily, DailyAdmin)
admin.site.register(SPMDaily, DailyAdmin)
admin.site.register(App3Daily, DailyAdmin)

admin.site.register(AppWeekly, WeeklyAdmin)
admin.site.register(FrameworkWeekly, WeeklyAdmin)
admin.site.register(DriverWeekly, WeeklyAdmin)
admin.site.register(ProtocolWeekly, WeeklyAdmin)
admin.site.register(SPMWeekly, WeeklyAdmin)
admin.site.register(App3Weekly, WeeklyAdmin)
