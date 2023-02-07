from django.test import TestCase
from users.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
import json
from django.utils.translation import gettext_lazy as _


class UsersTest(TestCase):

    fixtures = ['users.json']

    def test_create(self):
        resp = self.client.get(reverse('create_user'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='create.html')

        with open('users/fixtures/test_data.json', 'r') as user_info:
            new_user = json.load(user_info)[0]
            resp = self.client.post(
                reverse('create_user'),
                new_user
            )
            self.assertEqual(resp.status_code, 302)
            self.assertRedirects(resp, reverse('login_page'))

            user = User.objects.last()
            self.assertEqual(user.first_name, new_user.get('first_name'))
            self.assertEqual(user.last_name, new_user.get('last_name'))
            self.assertEqual(user.username, new_user.get('username'))

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
        self.assertRedirects(resp, f'/login/?next=/users/{user.id}/update/')
        self.assertFlashMessages(resp, _("You are not authorized!"))

        self.client.force_login(user)
        resp = self.client.get(
            reverse('update_user', kwargs={'pk': user.id})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='update.html')

        resp = self.client.get(
            reverse('update_user', kwargs={'pk': 2})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertFlashMessages(
            resp,
            _("You have't permission!")
        )

        with open('users/fixtures/test_data.json', 'r') as user_info:
            updated_user = json.load(user_info)[1]
            resp = self.client.post(
                reverse('update_user', kwargs={'pk': user.id}),
                updated_user
            )
            self.assertEqual(resp.status_code, 302)
            user.refresh_from_db()
            self.assertFlashMessages(
                resp=resp,
                message_text=_('User successfully changed'),
            )

            self.assertEqual(user.first_name, updated_user.get('first_name'))
            self.assertEqual(user.last_name, updated_user.get('last_name'))
            self.assertEqual(user.username, updated_user.get('username'))

    def test_delete(self):
        user = User.objects.get(username='jmurv')
        resp = self.client.get(reverse('delete_user', kwargs={'pk': user.id}))
        users_count = User.objects.count()
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f'/login/?next=/users/{user.id}/delete/')
        self.assertFlashMessages(resp, _("You are not authorized!"))

        self.client.force_login(user)

        resp = self.client.get(reverse('delete_user', kwargs={'pk': 2}))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('users_list'))
        self.assertEqual(User.objects.count(), users_count)
        self.assertFlashMessages(
            resp,
            _("You have't permission!")
        )

        resp = self.client.get(reverse('delete_user', kwargs={'pk': user.id}))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(
            reverse('delete_user', kwargs={'pk': user.id})
        )
        self.assertRedirects(resp, reverse('users_list'))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(User.objects.count(), users_count - 1)

    def assertFlashMessages(self, resp, message_text):
        messages = [
            message for message in map(str, get_messages(resp.wsgi_request))
        ]
        self.assertIn(message_text, messages)
