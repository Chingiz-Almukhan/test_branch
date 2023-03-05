from django.contrib import admin

from students.models import (FundsDebiting, MedicalCertificate, Payment,
                             StudentContract)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Payment._meta.fields]


@admin.register(StudentContract)
class StudentContractAdmin(admin.ModelAdmin):
    list_display = [field.name for field in StudentContract._meta.fields]


@admin.register(FundsDebiting)
class FundsDebitingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FundsDebiting._meta.fields]


@admin.register(MedicalCertificate)
class MedicalCertificateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MedicalCertificate._meta.fields]
