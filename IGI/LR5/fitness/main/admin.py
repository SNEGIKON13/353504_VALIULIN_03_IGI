from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Article, About, FAQ, Staff, Vacancy, Review, Promo, CustomUser,
    Gym, Equipment, Group, Membership, Attendance
)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'description')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question', 'answer')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'phone', 'email')
    search_fields = ('name', 'position')

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('is_active',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'created_at')
    search_fields = ('name', 'text')
    list_filter = ('rating',)

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'valid_from', 'valid_to', 'is_active')
    search_fields = ('code', 'description')
    list_filter = ('is_active',)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'birth_date', 'is_instructor', 'subscription')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_instructor', 'is_staff', 'subscription')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'birth_date', 'is_instructor', 'subscription', 'subscription_end')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone', 'birth_date', 'is_instructor', 'subscription', 'subscription_end')}),
    )

@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')
    search_fields = ('name', 'description')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'gym', 'quantity')
    search_fields = ('name', 'description')
    list_filter = ('gym',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'capacity', 'start_date', 'start_time', 'is_active')
    list_filter = ('is_active', 'start_date')
    search_fields = ('name', 'description')
    filter_horizontal = ('instructors',)  # Removed 'members' here

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'status', 'date_joined')
    list_filter = ('status', 'group')
    search_fields = ('user__username', 'group__name')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'session_date', 'attended')
    list_filter = ('attended', 'session_date', 'group')
    search_fields = ('user__username', 'group__name')