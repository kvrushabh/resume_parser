from django.contrib import admin
from .models import Profile

# Register your models here.

# admin.site.unregister(Group)
admin.site.register((Profile))