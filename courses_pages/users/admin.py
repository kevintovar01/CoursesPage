from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

#models
from .models import UserRole, User, Role, Country

class UserRoleInLine(admin.TabularInline):
    # Inline using the through model for the User.roles M2M
    model = UserRole
    fk_name = 'user'
    extra = 1


@admin.register(User)
class MyUserAdmin(UserAdmin):
    inlines = [UserRoleInLine]
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    ordering = ('email',)
    filter_horizontal = ()
    search_fields = ('email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'born_date', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'born_date', 'country', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__email', 'role__name')

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
