from django.test import TestCase
from manager.models import User
from django.urls import reverse


class UsersTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            first_name='Vladimir',
            last_name='Zhmur',
            username='jmurv',
            email='architect.lock@outlook.com',
            password='794613825Zx'
        )
        User.objects.create(
            first_name='Anastasiya',
            last_name='Kolupaeva',
            username='Homyak07',
            email='anastasiyakolupaeva@mail.ru',
            password='794613825Ak'
        )

    def test_register(self):
        resp = self.client.get(reverse('create_user'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='create.html')

        resp = self.client.post(
            reverse('create_user'),
            {
                'first_name': 'Vladimir',
                'last_name': 'Epshteyn',
                'username': 'pussydestroyer228',
                'password1': '794613825Ve',
                'password2': '794613825Ve',
            }
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('login_page'))

        user = User.objects.last()
        self.assertEqual(user.first_name, 'Vladimir')
        self.assertEqual(user.last_name, 'Epshteyn')
        self.assertEqual(user.username, 'pussydestroyer228')
