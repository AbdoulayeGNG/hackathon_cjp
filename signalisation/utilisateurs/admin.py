from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'last_login')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Informations personnelles'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
        (_('Dates importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    
    actions = ['make_staff', 'remove_staff', 'activate_users', 'deactivate_users']
    
    def make_staff(self, request, queryset):
        queryset.update(is_staff=True)
    make_staff.short_description = "Donner les droits d'administration aux utilisateurs sélectionnés"
    
    def remove_staff(self, request, queryset):
        queryset.update(is_staff=False)
    remove_staff.short_description = "Retirer les droits d'administration aux utilisateurs sélectionnés"
    
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "Activer les utilisateurs sélectionnés"
    
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "Désactiver les utilisateurs sélectionnés"
