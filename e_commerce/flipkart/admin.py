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


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'needed_for', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'category__name', 'needed_for')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active', 'is_show_top_poduct', 'created_at')
    list_filter = ('category', 'is_active', 'is_show_top_poduct', 'created_at')
    search_fields = ('name', 'category__name')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'start_at', 'end_at', 'created_at')
    search_fields = ('title', 'message')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'role', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('employee_name', 'role')


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'caption')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone', 'subject', 'message')
