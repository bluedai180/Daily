from django.contrib import admin

from django.contrib import admin

from .models import Team, User, AppDaily


class UserAdmin(admin.ModelAdmin):
    # fields = ["name", "email", "team"]
    list_display = ("name", "email", "team", "permission")

admin.site.register([Team, AppDaily])
admin.site.register(User, UserAdmin)
