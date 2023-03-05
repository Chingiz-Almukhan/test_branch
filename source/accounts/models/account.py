from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import AccountManager

from education.models import Grouping, StudentGrouping, Subject, TeacherGrouping

from lessons.models import Lesson

from students.models import StudentContract


class Account(AbstractUser):
    email = models.EmailField(verbose_name='Электронная почта', unique=True, blank=True)
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to='avatars',
        verbose_name='Аватар',
    )
    username = None
    phone_number = PhoneNumberField(
        unique=True,
        null=False,
        blank=False,
    )
    application = models.ForeignKey(
        verbose_name="Заявка",
        to='applications.Application',
        related_name='accounts',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )
    birth_date = models.DateField(verbose_name='Дата рождения', max_length=10, null=True, blank=True)
    iin = models.CharField(verbose_name='ИИН', null=True, blank=True, max_length=12)
    address = models.CharField(verbose_name='Адрес проживания', max_length=200, null=True, blank=True)
    sex = models.CharField(verbose_name='Пол', max_length=6, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def get_active_student_groupings(self):
        """Получить все активные зачисления в группу"""
        student_groupings = StudentGrouping.objects.filter(student=self, is_active=True)
        return student_groupings

    def get_active_groupings(self):
        """Получить все активные группы студента"""
        student_groupings = self.get_active_student_groupings()
        groupings = Grouping.objects.filter(student_grouping__in=student_groupings)
        return groupings

    def get_all_conducted_lessons(self):
        """Получить все проведенные занятия для студента"""
        groupings = self.study_groupings.all()
        #  TODO отфильтровать занятия по периоду обучения студента в данных группах
        lessons = Lesson.objects.filter(grouping__in=groupings, is_conducted=True)
        return lessons

    def get_active_contract(self):
        """Получить текущий контракт студента"""
        try:
            contract = StudentContract.objects.get(student=self, is_active=True)
        except BaseException:
            contract = None
        return contract

    def get_current_subjects(self):
        """Получить текущие предметы студента"""
        if self.get_active_contract():
            subjects = self.get_active_contract().subjects.all()
        else:
            subjects = Subject.objects.none()
        return subjects

    def __str__(self):
        return f'{self.get_full_name()}'


class Teacher(models.Model):
    account = models.OneToOneField(to='accounts.Account', verbose_name='Аккаунт', related_name='teacher',
                                   on_delete=models.CASCADE, null=False, blank=False)
    education = models.CharField(verbose_name='Образование', null=True, blank=True, max_length=500)
    subjects = models.ManyToManyField(to='education.Subject', related_name='teacher_subject')

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    def get_active_teacher_groupings(self):
        """Получить все активные зачисления в группу"""
        teacher_groupings = TeacherGrouping.objects.filter(teacher=self, is_active=True)
        return teacher_groupings

    def __str__(self):
        return f'{self.account.get_full_name()}'
