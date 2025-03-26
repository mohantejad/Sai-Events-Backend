from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User, Address


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = '__all__'


class AddressInline(admin.StackedInline):
    model = Address
    extra = 1
    filter_horizontal = ()


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    inlines = [AddressInline]

    list_display = ['email', 'first_name', 'last_name', 'user_type', 'is_active', 'is_staff']
    list_filter = ["is_superuser", 'is_staff', 'user_type']
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)
    fieldsets = (
        (_("Personal Info"), {"fields": ("first_name", "last_name", "email", "phone_number", "profile_picture", "user_type")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "phone_number", "password1", "password2"],
            },
        ),
    ]


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)