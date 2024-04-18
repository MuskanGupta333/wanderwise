from django.contrib import admin
from .models import User
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name",)

admin.site.register(User)
