from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

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


@admin.register(sliderImage)
class sliderImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'category__name')
