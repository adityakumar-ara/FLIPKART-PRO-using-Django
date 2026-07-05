from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

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
    list_display = ('image_tag', 'name', 'sku', 'stock', 'price', 'is_active')
    list_filter = ('category', 'is_active', 'is_owner_selected', 'created_at')
    search_fields = ('name', 'sku')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_tag.short_description = 'Image'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'not_show', 'created_at', 'updated_at')
    list_filter = ('not_show', 'created_at', 'updated_at')
    search_fields = ('user__username', 'product__name')


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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'total_amount', 'payment_method', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('payment_method', 'status', 'created_at')
    search_fields = ('user__username', 'full_name', 'email')
    actions = ['mark_as_processing', 'mark_as_completed', 'mark_as_cancelled']

    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')
    mark_as_processing.short_description = "Mark selected orders as Processing"

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark selected orders as Completed"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = "Mark selected orders as Cancelled"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'subtotal')
    search_fields = ('order__id', 'product__name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'status', 'created_at')
    list_filter = ('status', 'rating', 'created_at')
    search_fields = ('user__username', 'product__name', 'comment')
    actions = ['approve_reviews', 'reject_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(status='approved')
    approve_reviews.short_description = "Mark selected reviews as Approved"

    def reject_reviews(self, request, queryset):
        queryset.update(status='rejected')
    reject_reviews.short_description = "Mark selected reviews as Rejected"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone', 'subject', 'message')
