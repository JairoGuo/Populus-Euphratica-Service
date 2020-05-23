from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from sonsuz_website.users.forms import UserChangeForm, UserCreationForm
from .models import Homepages

User = get_user_model()

class HomePageAdmin(admin.ModelAdmin):
    fields = ['user', 'homepage_type', 'homepage_url']

class HomePageAdmin1(admin.TabularInline):
    extra = 1 # 默认为3
    model = Homepages

# class SKillAdmin(admin.TabularInline):
#     extra = 1 # 默认为3
#     model = Skill

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name", 'website', 'avatar', 'introduction')}),) + auth_admin.UserAdmin.fieldsets
    # inlines = [HomePageAdmin1, SKillAdmin]
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]



admin.site.register(Homepages, HomePageAdmin)
