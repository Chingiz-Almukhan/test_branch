from django.contrib import admin

from accounts.models.account import Account, Teacher


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Account._meta.fields]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Teacher._meta.fields]
