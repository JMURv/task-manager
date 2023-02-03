from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from statuses.models import Status
from django.contrib.auth import get_user_model


class StatusTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']

    def setUp(self):
        self.user = get_user_model().objects.first()
        self.client.force_login(self.user)

    def test_list(self):
        resp = self.client.get(reverse('status_list'))
        self.assertTrue(len(resp.context['object_list']) == 1)

    def test_create(self):
        resp = self.client.post(reverse('create_status'), {'name': 'status2'})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('status_list'))
        self.get_messages(resp, 'Статус успешно создан')

        resp = self.client.get(reverse('status_list'))
        self.assertTrue(len(resp.context['object_list']) == 2)

    def test_update(self):
        tested_status = Status.objects.get(name='status_1')
        self.assertEqual(tested_status.name, 'status_1')

        resp = self.client.post(
            path=reverse('update_status', kwargs={'pk': tested_status.id}),
            data={'name': 'UpdatedName'}
        )

        self.assertEqual(resp.status_code, 302)
        tested_status.refresh_from_db()
        self.assertEqual(tested_status.name, 'UpdatedName')
        self.get_messages(resp, 'Статус успешно изменён')

    def test_delete_status(self):
        tested_status = Status.objects.get(name='status_1')
        self.assertEqual(Status.objects.count(), 1)
        resp = self.client.post(
            path=reverse('delete_status', kwargs={'pk': tested_status.id})
        )
        self.assertEqual(resp.status_code, 302)
        self.get_messages(
            resp,
            'Невозможно удалить статус, потому что он используется'
        )

        self.assertEqual(Status.objects.count(), 1)
        # Создаём новый статус
        resp = self.client.post(reverse('create_status'), {'name': 'status2'})
        self.assertRedirects(resp, reverse('status_list'))
        resp = self.client.get(reverse('status_list'))
        self.assertTrue(len(resp.context['object_list']) == 2)
        # Удаляем новый статус
        tested_status = Status.objects.get(name='status2')
        resp = self.client.post(
            path=reverse('delete_status', kwargs={'pk': tested_status.id})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Status.objects.count(), 1)

        self.get_messages(resp, 'Статус успешно удалён')

    def get_messages(self, resp, message_text, count=1):
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(len(messages), count)
        self.assertEqual(str(messages[0]), message_text)
