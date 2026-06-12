from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Details', {
            'fields': (
                'full_name', 'mobile_no', 'dob', 'address', 'alternate_mobile_no', 'profile_image', 'gender',
            )
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Details', {
            'fields': (
                'full_name', 'email','mobile_no','dob','address','alternate_mobile_no','profile_image','gender',
            )
        }),
    )
    list_display = ('username', 'full_name', 'email', 'mobile_no', 'gender', 'is_staff')
    search_fields = ('username', 'full_name', 'email', 'mobile_no')
