from django.contrib.auth.models import Group
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Account


class TestStudentView(TestCase):

    def setUp(self):
        Group.objects.create(name='admin')
        Group.objects.create(name='student')
        Group.objects.create(name='teacher')
        test_user = Account.objects.create(
            email='test@test.test',
            phone_number='+77774441122',
        )
        test_user.set_password('testpass')
        test_user.save()
        self.client_anonim = Client()
        self.client_login = Client()
        self.client_login.login(email='test@test.test', password='testpass')

        return super().setUp()

    def test_student_list_get(self):
        response = self.client_anonim.get(reverse('students'))
        self.assertAlmostEquals(response.status_code, 302)

        response = self.client_login.get(reverse('students'))
        self.assertAlmostEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/admin/students.html')

    def test_student_detail_get(self):
        response = self.client_anonim.get(reverse('student', args=['1']))
        self.assertAlmostEquals(response.status_code, 302)

        response = self.client_login.get(reverse('student', args=['1']))
        self.assertAlmostEquals(response.status_code, 200)
