from django.contrib import admin

from lessons.models import Homework, Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Lesson._meta.fields]

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Homework._meta.fields]
