# Generated by Django 4.1.3 on 2023-02-15 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0003_application_contract_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='contract_date',
            field=models.DateField(auto_now=True, null=True, verbose_name='Дата контракта'),
        ),
    ]
