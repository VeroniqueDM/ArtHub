from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from ArtHub.accounts.models import ArtHubUser, UserProfile, Artist, ArtModUser, RegularUser


# @admin.register(ArtistProfile)
# class ArtistProfileAdmin(admin.ModelAdmin):
#
#     list_display = ('first_name', 'last_name')

@admin.register(UserProfile)
class RegularProfileAdmin(admin.ModelAdmin):

    list_display = ('first_name', 'last_name')

@admin.register(ArtHubUser)
class ArtHubUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions')
    list_display = ('username', 'type', )
    fieldsets = (
        (None, {'fields': ('username', 'type')}),
        # Other fieldsets
        ('Permissions', {'fields': ('is_staff', 'groups', 'user_permissions')}),
        # ('Group Permissions', {
        #     'classes': ('collapse',),
        #     'fields': ('groups', 'user_permissions',)
        # }),
    )


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions')
    list_display = ('username', )
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_staff', 'groups', 'user_permissions')}),
    )


@admin.register(ArtModUser)
class ArtModUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions')
    list_display = ('username', )
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_staff', 'groups', 'user_permissions')}),
    )

@admin.register(RegularUser)
class RegularUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions')
    list_display = ('username', )
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_staff', 'groups', 'user_permissions')}),
    )
