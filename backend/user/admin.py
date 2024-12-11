from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .collection.models import CollectionGroup, Collection, GroupCollection

# Register your models here.
admin.site.register(User, UserAdmin)

admin.site.register(Collection)
admin.site.register(CollectionGroup)
admin.site.register(GroupCollection)
