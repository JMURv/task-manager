from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from statuses.models import Status
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import json


class StatusTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']

    def setUp(self):
        self.user = get_user_model().objects.first()
        self.client.force_login(self.user)

    def test_list(self):
        resp = self.client.get(reverse('status_list'))
        self.assertTrue(len(resp.context['object_list']) == 1)

    def test_create(self):
        status_count = Status.objects.count()
        with open('statuses/fixtures/test_data.json', 'r') as status_info:
            new_status = json.load(status_info)[0]
            resp = self.client.post(reverse('create_status'), new_status)
            self.assertEqual(resp.status_code, 302)
            self.assertRedirects(resp, reverse('status_list'))
            self.assertFlashMessages(resp, _("Status created successfully"))

        resp = self.client.get(reverse('status_list'))
        self.assertTrue(len(resp.context['object_list']) == status_count+1)

    def test_update(self):
        tested_status = Status.objects.get(name='status_1')
        self.assertEqual(tested_status.name, 'status_1')

        with open('statuses/fixtures/test_data.json', 'r') as status_info:
            updated_status = json.load(status_info)[1]
            resp = self.client.post(
                path=reverse('update_status', kwargs={'pk': tested_status.id}),
                data=updated_status
            )

            self.assertEqual(resp.status_code, 302)
            tested_status.refresh_from_db()
            self.assertEqual(tested_status.name, updated_status.get('name'))
            self.assertFlashMessages(resp, _('Status successfully changed'))

    def test_delete_status(self):
        tested_status = Status.objects.get(name='status_1')
        status_count = Status.objects.count()
        resp = self.client.post(
            path=reverse('delete_status', kwargs={'pk': tested_status.id})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertFlashMessages(
            resp,
            _("Can't delete, status in use")
        )

        self.assertEqual(Status.objects.count(), status_count)
        # Создаём новый статус
        resp = self.client.post(reverse('create_status'), {'name': 'status2'})
        self.assertRedirects(resp, reverse('status_list'))
        resp = self.client.get(reverse('status_list'))
        self.assertTrue(len(resp.context['object_list']) == status_count+1)
        # Удаляем новый статус
        tested_status = Status.objects.get(name='status2')
        resp = self.client.post(
            path=reverse('delete_status', kwargs={'pk': tested_status.id})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Status.objects.count(), status_count)

        self.assertFlashMessages(resp, _('Status successfully deleted'))

    def assertFlashMessages(self, resp, message_text):
        messages = [
            message for message in map(str, get_messages(resp.wsgi_request))
        ]
        self.assertIn(message_text, messages)
