from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
<<<<<<< HEAD
    list_display = ['email', 'username', 'is_staff']
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('name',)}), )
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('name', )}), )


admin.site.register(CustomUser, CustomUserAdmin)
=======

    list_display = ['email', 'username', 'is_staff']
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('name', )}), )
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('name', )}), )


admin.site.register(CustomUser, CustomUserAdmin)
>>>>>>> b2368c7 (wiederherstellung)
