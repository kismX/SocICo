from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Profile, Friendship

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'is_superuser']
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('name',)}), )
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('name', )}), )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Friendship)
