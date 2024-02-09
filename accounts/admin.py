from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import *

# Register your models here.


class UserAdminConfig(UserAdmin):
    model = CustomUser
    search_fields = ('full_name', 'mobile_number')
    list_filter = ('full_name', 'mobile_number')
    ordering = ('-id',)
    list_display = ('mobile_number',)
    fieldsets = (
        ("Details", {'fields': ('user_type', 'full_name','mobile_number', 'email', 'address', 'birth_date', 
                                'status','is_verified', 'gender')}),
        ('Permissions', {'fields': ('is_staff', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_type', 'full_name', 'mobile_number', 'is_staff')}
         ),
    )


admin.site.register(CustomUser, UserAdminConfig)


