from django.contrib import admin
from accounts.models import Person, Manager


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("username",  "contact_email", "contact_phone")
    search_fields = ('name',)


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ("manager",)