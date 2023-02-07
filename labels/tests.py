from django.test import TestCase
from labels.models import Label
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.utils.translation import gettext_lazy as _
import json


class LabelsTest(TestCase):
    fixtures = ['users.json', 'labels.json', 'tasks.json', 'statuses.json']

    def setUp(self) -> None:
        self.user = get_user_model().objects.first()
        self.client.force_login(self.user)

    def test_list(self):
        resp = self.client.get(
            path=reverse('label_list')
        )
        self.assertEqual(len(resp.context['object_list']), 3)

    def test_create(self):
        labels_count = Label.objects.count()
        with open('labels/fixtures/test_data.json', 'r') as label_info:
            new_label = json.load(label_info)[0]
            resp = self.client.post(
                path=reverse('label_create'),
                data=new_label
            )
            self.assertEqual(resp.status_code, 302)
            self.assertRedirects(resp, reverse('label_list'))
            self.assertFlashMessages(resp, _("Label created successfully"))
        resp = self.client.get(
            path=reverse('label_list')
        )
        self.assertEqual(len(resp.context['object_list']), labels_count + 1)

    def test_update(self):
        tested_label = Label.objects.get(name='label_1')
        with open('labels/fixtures/test_data.json', 'r') as label_info:
            new_label = json.load(label_info)[1]
            resp = self.client.post(
                path=reverse('label_update', kwargs={'pk': tested_label.id}),
                data=new_label
            )
            self.assertEqual(resp.status_code, 302)
            self.assertFlashMessages(resp, _('Label successfully changed'))
            tested_label.refresh_from_db()
            self.assertEqual(tested_label.name, new_label.get('name'))

    def test_delete(self):
        labels_count = Label.objects.count()
        tested_label = Label.objects.get(name='label_1')
        # Пытаемся удалить метку, прикрепленную к задаче
        resp = self.client.post(
            path=reverse('label_delete', kwargs={'pk': tested_label.id})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('label_list'))
        self.assertEqual(Label.objects.count(), labels_count)
        self.assertFlashMessages(
            resp,
            _("Can't delete, label in use")
        )
        # Метка, не прикрепленная к задаче
        tested_label = Label.objects.get(name='label_3')
        resp = self.client.post(
            path=reverse('label_delete', kwargs={'pk': tested_label.id})
        )
        self.assertFlashMessages(resp, _('Label successfully deleted'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('label_list'))
        self.assertEqual(Label.objects.count(), labels_count - 1)

    def assertFlashMessages(self, resp, message_text):
        messages = [
            message for message in map(str, get_messages(resp.wsgi_request))
        ]
        self.assertIn(message_text, messages)
