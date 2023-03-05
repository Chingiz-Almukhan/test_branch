from django.db import models


class Payment(models.Model):
    student = models.ForeignKey(to='accounts.Account', on_delete=models.RESTRICT, related_name='payments')
    date = models.DateField(verbose_name='Дата платежа', null=True)
    amount = models.PositiveIntegerField(verbose_name='Сумма платежа')
    author = models.ForeignKey(to='accounts.Account', on_delete=models.RESTRICT, related_name='author_payments')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-date']

    def __str__(self):
        return f'{self.student} - {self.date} - {self.amount} тенге'


class StudentContract(models.Model):
    student = models.ForeignKey(to='accounts.Account', on_delete=models.CASCADE, related_name='student_contracts')
    signing_date = models.DateField(verbose_name='Дата подписания')
    start_date = models.DateField(verbose_name='Дата начала обучения')
    end_date = models.DateField(verbose_name='Дата окончания обучения', null=True, blank=True)
    contract = models.FileField(verbose_name="Подписанный договор", null=True, blank=True,
                                help_text="Загружать pdf подписанного договора", upload_to='contracts/')
    subjects = models.ManyToManyField(to='education.Subject', related_name='contracts', blank=True)
    amount = models.PositiveIntegerField(verbose_name='Сумма договора')
    is_active = models.BooleanField(verbose_name='Действующий')

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договора'

    def __str__(self):
        return f'{self.student} - {self.signing_date}'


class FundsDebiting(models.Model):
    """Фактическое ежемесячное списания средств за обучение
    amount будет рассчитываться с учетом суммы договора минус стоимость
    непосещенных занятий по справкам
    """
    student = models.ForeignKey(to='accounts.Account', on_delete=models.CASCADE, related_name='student_fund_debitings')
    date = models.DateField(verbose_name='Дата списания')
    period = models.DateField(verbose_name='Списание за месяц')
    amount = models.PositiveIntegerField(verbose_name='Сумма к списанию')

    class Meta:
        verbose_name = "Списание средств"
        verbose_name_plural = "Списания средств"
        ordering = ['-period']

    def __str__(self):
        return f'{self.student} - {self.period}'


class MedicalCertificate(models.Model):
    """больничные листы ученика"""
    student = models.ForeignKey(to='accounts.Account', on_delete=models.CASCADE, related_name='medical_certificates')
    start_date = models.DateField(verbose_name='Дата начала больничного')
    end_date = models.DateField(verbose_name='Дата окончания больничного')
    author = models.ForeignKey(to='accounts.Account', on_delete=models.CASCADE,
                               related_name='author_medical_certificate')
    attachment = models.FileField(verbose_name="Вложение", null=True, blank=True,
                                  help_text="Загрузить больничный лист", upload_to='medical_certificat/')

    class Meta:
        verbose_name = "Больничный лист"
        verbose_name_plural = "Больничные листы"

    def __str__(self):
        return f'Больничный лист - {self.student}'
