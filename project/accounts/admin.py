from django.contrib import admin
from .models import *
# Register your models here.


class prof_data(admin.ModelAdmin):
    list_display = ['user']

admin.site.register(Profile , prof_data)