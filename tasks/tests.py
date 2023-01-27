from django.test import TestCase
from django.urls import reverse
from users.models import User
from tasks.models import Task
from statuses.models import Status
from labels.models import Label


class TasksTest(TestCase):
    def setUp(self) -> None:
        User.objects.create(
            first_name='Vladimir',
            last_name='Zhmur',
            username='jmurv',
            email='architect.lock@outlook.com',
            password='794613825Zx'
        )
        Label.objects.create(name='label_1')
        Status.objects.create(name='status_1')

        self.user = User.objects.get(username='jmurv')
        self.label = Label.objects.get(name='label_1')
        self.status = Status.objects.get(name='status_1')
        self.urls = [
            reverse('list_task'),
            reverse('task_create'),
            reverse('task_update', kwargs={'pk': 1}),
            reverse('task_delete', kwargs={'pk': 1}),
            reverse('task_detail', kwargs={'pk': 1})
        ]

        Task.objects.create(
            name='TestTask',
            description='TestDescription',
            creator=self.user,
            executor=self.user,
            status=self.status,
        )

    def test_get_req(self):
        self.client.force_login(self.user)
        for url in self.urls:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)
