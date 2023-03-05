# Generated by Django 4.1.3 on 2023-02-04 17:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("education", "0001_initial"),
        ("students", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StudentContract",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("signing_date", models.DateField(verbose_name="Дата подписания")),
                ("start_date", models.DateField(verbose_name="Дата начала обучения")),
                ("end_date", models.DateField(verbose_name="Дата окончания обучения")),
                (
                    "contract",
                    models.FileField(
                        blank=True,
                        help_text="Загружать pdf подписанного договора",
                        null=True,
                        upload_to="contracts/",
                        verbose_name="Подписанный договор",
                    ),
                ),
                ("amount", models.PositiveIntegerField(verbose_name="Сумма договора")),
                ("is_active", models.BooleanField(verbose_name="Действующий")),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="student_contracts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "subjects",
                    models.ManyToManyField(
                        blank=True, related_name="contracts", to="education.subject"
                    ),
                ),
            ],
            options={
                "verbose_name": "Договор",
                "verbose_name_plural": "Договора",
            },
        ),
    ]
