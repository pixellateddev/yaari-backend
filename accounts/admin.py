from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Verification

admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(Verification)
