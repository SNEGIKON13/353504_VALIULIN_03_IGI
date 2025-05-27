from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Article, About, FAQ, Staff, Vacancy, Review, Promo, CustomUser, Gym, Equipment, Service, Group, Session, Membership, Attendance, ServiceBooking

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
    list_display = ('username', 'email', 'phone', 'age', 'is_instructor')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_instructor', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'age', 'is_instructor')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone', 'age', 'is_instructor')}),
    )

@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')
    search_fields = ('name',)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'gym', 'quantity')
    list_filter = ('gym',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'gym', 'start_date', 'end_date', 'price')
    list_filter = ('service', 'gym')
    filter_horizontal = ('instructors',)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('group', 'start_time', 'end_time')
    list_filter = ('group',)
    filter_horizontal = ('instructors',)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'group')
    search_fields = ('user__username',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('session', 'member', 'attended')
    list_filter = ('attended', 'session')

@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'preferred_date', 'status', 'created_at')
    list_filter = ('status', 'service')
    search_fields = ('user__username', 'service__name', 'notes')
    raw_id_fields = ('user', 'service')
    readonly_fields = ('created_at', 'updated_at')
