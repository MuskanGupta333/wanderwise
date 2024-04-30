from django.contrib import admin

# Register your models here.

from .models import Profile,Guide, VisitPlan,RateBit,Feedback

# class ProfileAdmin(admin.ModelAdmin):


admin.site.register(Profile)
admin.site.register(Guide)
admin.site.register(VisitPlan)
admin.site.register(RateBit)
admin.site.register(Feedback)



