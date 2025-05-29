from datetime import date
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import (
    Article, About, FAQ, Staff, Vacancy, Review, Promo, CustomUser,
    Gym, Equipment, Group, Membership, Attendance
)

class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if self.instance and self.instance.is_superuser:
            return birth_date
            
        if not birth_date:
            raise forms.ValidationError('Дата рождения обязательна.')
            
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise forms.ValidationError('Пользователь должен быть старше 18 лет.')
        return birth_date

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
    form = CustomUserAdminForm
    list_display = ('username', 'email', 'phone', 'birth_date', 'is_instructor', 'subscription')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_instructor', 'is_staff', 'subscription')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'birth_date', 'is_instructor', 'subscription', 'subscription_end')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone', 'birth_date', 'is_instructor', 'subscription', 'subscription_end')}),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.is_instructor:
            # Удаляем поля абонемента для инструкторов
            additional_fields = ('phone', 'birth_date', 'is_instructor')
        else:
            additional_fields = ('phone', 'birth_date', 'is_instructor', 'subscription', 'subscription_end')
        
        # Обновляем последний fieldset с Additional Info
        fieldsets = list(fieldsets)
        fieldsets[-1] = ('Additional Info', {'fields': additional_fields})
        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.is_instructor:
            if 'subscription' in form.base_fields:
                del form.base_fields['subscription']
            if 'subscription_end' in form.base_fields:
                del form.base_fields['subscription_end']
        return form

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