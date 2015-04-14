from django.contrib import admin
from draw.models import student
# Register your models here.

class studentAdmin(admin.ModelAdmin):
    list = ('stuName','IDCard','stuNum')

admin.site.register(student, studentAdmin)