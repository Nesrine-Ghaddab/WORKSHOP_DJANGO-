from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, organizing_comitee
# Register your models here.
class OrganizingComiteeInline(admin.TabularInline):
    model = organizing_comitee
    extra = 1
    autocomplete_fields = ['conference_id']
    readonly_fields = ('created_at', 'updated_at')


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('user_id', 'username', 'first_name', 'last_name', 'email', 'role', 'affiliation', 'nationality', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'nationality')
    list_filter = ('role', 'nationality', 'created_at')
    ordering = ('created_at',)
    readonly_fields = ('user_id', 'created_at', 'updated_at')

    fieldsets = (
        ("User Information", {
            'fields': ('user_id', 'username', 'first_name', 'last_name', 'email', 'affiliation', 'nationality', 'role')
        }),
        ("Permissions", {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ("Timestamps", {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role', 'affiliation', 'nationality'),
        }),
    )

    inlines = [OrganizingComiteeInline]



@admin.register(organizing_comitee)
class OrganizingComiteeAdmin(admin.ModelAdmin):
    list_display = ('comitee_id', 'user_id', 'conference_id', 'role_in_comitee', 'date_join')
    search_fields = ('user_id__username', 'conference_id__title', 'role_in_comitee')
    list_filter = ('role_in_comitee', 'date_join')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['user_id', 'conference_id']
