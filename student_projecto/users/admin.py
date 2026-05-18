from django.contrib import admin
from .models import Branch, CustomUser, Subject, Student, Group, SubscriptionPlan, PricingGrid, Lesson, Attendance

admin.site.register(Branch)
admin.site.register(CustomUser)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(SubscriptionPlan)
admin.site.register(PricingGrid)
admin.site.register(Lesson)
admin.site.register(Attendance)