from django.test import TestCase
from users.models import User
from django.urls import reverse


class UsersTest(TestCase):

    fixtures = ['users.json']

    def test_create(self):
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

        resp = self.client.get(reverse('users_list'))
        self.assertTrue(len(resp.context['user_list']) == 3)

    def test_read(self):
        resp = self.client.get(reverse('users_list'))
        self.assertTrue(len(resp.context['user_list']) == 2)

    def test_update(self):
        user = User.objects.get(username='jmurv')
        resp = self.client.get(
            reverse('update_user', kwargs={'pk': user.id})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('login_page'))

        self.client.force_login(user)
        resp = self.client.get(
            reverse('update_user', kwargs={'pk': user.id})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='update.html')

        resp = self.client.post(
            reverse('update_user', kwargs={'pk': user.id}),
            {
                'first_name': 'TestName',
                'last_name': 'TestLastName',
                'username': 'TestUsername',
                'password1': 'TestPassword123',
                'password2': 'TestPassword123',
            }
        )
        self.assertEqual(resp.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'TestName')
        self.assertEqual(user.last_name, 'TestLastName')
        self.assertEqual(user.username, 'TestUsername')

    def test_delete(self):
        user = User.objects.get(username='jmurv')
        resp = self.client.get(reverse('delete_user', kwargs={'pk': user.id}))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('login_page'))

        self.client.force_login(user)

        resp = self.client.get(reverse('delete_user', kwargs={'pk': 2}))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('users_list'))
        self.assertEqual(User.objects.count(), 2)

        resp = self.client.get(reverse('delete_user', kwargs={'pk': user.id}))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(
            reverse('delete_user', kwargs={'pk': user.id})
        )
        self.assertRedirects(resp, reverse('users_list'))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
