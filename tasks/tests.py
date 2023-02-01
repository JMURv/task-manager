from django.test import TestCase
from django.urls import reverse
from statuses.models import Status
from labels.models import Label
from django.contrib.auth import get_user_model


class TasksTest(TestCase):

    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']

    def setUp(self) -> None:
        self.user = get_user_model().objects.first()
        self.label = Label.objects.get(name='label_1')
        self.status = Status.objects.get(name='status_1')
        self.urls = [
            reverse('list_task'),
            reverse('task_create'),
            reverse('task_update', kwargs={'pk': 1}),
            reverse('task_delete', kwargs={'pk': 1}),
            reverse('task_detail', kwargs={'pk': 1})
        ]

    def test_get_req(self):
        self.client.force_login(self.user)
        for url in self.urls:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)
