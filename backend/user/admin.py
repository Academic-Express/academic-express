from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .collection.models import Collection, CollectionGroup, GroupCollection
from .models import User

# Register your models here.
admin.site.register(User, UserAdmin)

admin.site.register(Collection)
admin.site.register(CollectionGroup)
admin.site.register(GroupCollection)
