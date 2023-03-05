from django.db import models


class Lesson(models.Model):
    date = models.DateField(verbose_name='Дата проведения')
    grouping = models.ForeignKey(to='education.Grouping', on_delete=models.CASCADE, related_name='lessons')
    auditorium = models.ForeignKey(to='education.Auditorium', on_delete=models.CASCADE, related_name='lessons')
    class_time = models.ForeignKey(to='education.ClassTime', related_name='lessons',
                                   on_delete=models.CASCADE, null=True, verbose_name='Номер урока')
    teacher = models.ForeignKey(to='accounts.Teacher', on_delete=models.CASCADE,
                                related_name='lessons', null=True, blank=True)
    topic = models.TextField(verbose_name='Тема урока', null=True, blank=True)
    is_conducted = models.BooleanField(verbose_name='Проведен', default=False)
    homework = models.ForeignKey(to='lessons.Homework', on_delete=models.SET_NULL,
                                 related_name='lessons', null=True, blank=True)
    students_visited = models.ManyToManyField(to='accounts.Account', related_name='lessons_visited',
                                              verbose_name='Присутствовавшие студенты', blank=True)

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'

    def __str__(self):
        return f'{self.grouping.name} - {self.date}'


class Homework(models.Model):
    task = models.TextField(verbose_name='Задание')
    attachment = models.FileField(verbose_name="Вложение", null=True, blank=True,
                                  help_text="Загрузить домашнее задание", upload_to='homework/')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'

    def __str__(self):
        return self.task[:10]
