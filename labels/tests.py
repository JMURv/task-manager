from django.test import TestCase
from labels.models import Label
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages


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
        resp = self.client.post(
            path=reverse('label_create'),
            data={'name': 'TestLabelName'}
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('label_list'))
        self.get_messages(resp, 'Метка успешно создана')
        resp = self.client.get(
            path=reverse('label_list')
        )
        self.assertEqual(len(resp.context['object_list']), 4)

    def test_update(self):
        tested_label = Label.objects.get(name='label_1')
        resp = self.client.post(
            path=reverse('label_update', kwargs={'pk': tested_label.id}),
            data={'name': 'UpdateLabelName'}
        )
        self.assertEqual(resp.status_code, 302)
        self.get_messages(resp, 'Метка успешно изменена')
        tested_label.refresh_from_db()
        self.assertEqual(tested_label.name, 'UpdateLabelName')

    def test_delete(self):
        tested_label = Label.objects.get(name='label_1')
        self.assertEqual(Label.objects.count(), 3)
        # Пытаемся удалить метку, прикрепленную к задаче
        resp = self.client.post(
            path=reverse('label_delete', kwargs={'pk': tested_label.id})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('label_list'))
        self.assertEqual(Label.objects.count(), 3)
        self.get_messages(
            resp,
            'Невозможно удалить метку, потому что она используется'
        )
        # Метка, не прикрепленная к задаче
        tested_label = Label.objects.get(name='label_3')
        resp = self.client.post(
            path=reverse('label_delete', kwargs={'pk': tested_label.id})
        )
        self.get_messages(resp, 'Метка успешно удалена')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('label_list'))
        self.assertEqual(Label.objects.count(), 2)

    def get_messages(self, resp, message_text, count=1):
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(len(messages), count)
        self.assertEqual(str(messages[0]), message_text)
