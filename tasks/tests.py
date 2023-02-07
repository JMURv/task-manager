from django.test import TestCase
from django.urls import reverse
from statuses.models import Status
from labels.models import Label
from users.models import User
from tasks.models import Task
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.utils.translation import gettext_lazy as _
import json


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
        self.user = User.objects.get(username='jmurv')
        self.client.force_login(self.user)

    def test_get_req(self):
        self.client.force_login(self.user)
        for url in self.urls:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)

    def test_create_task(self):
        tasks_count = Task.objects.count()
        with open('tasks/fixtures/test_data.json', 'r') as task_info:
            create_task = json.load(task_info)[0]
            resp = self.client.post(
                reverse('task_create'),
                data=create_task
            )
            self.assertEqual(resp.status_code, 302)
            self.assertFlashMessages(resp, _("Task created successfully"))
            self.assertRedirects(resp, reverse('list_task'))

            resp = self.client.get(reverse('list_task'))
            self.assertTrue(
                len(resp.context['object_list']) == tasks_count + 1)

    def test_update_task(self):
        with open('tasks/fixtures/test_data.json', 'r') as task_info:
            new_task = json.load(task_info)[1]
            resp = self.client.post(
                reverse('task_update', kwargs={'pk': 1}),
                data=new_task
            )
            self.assertEqual(resp.status_code, 302)
            self.assertRedirects(resp, reverse('list_task'))
            self.assertFlashMessages(resp, _('Task successfully changed'))

            task = Task.objects.get(name='UpdatedName')
            self.assertEqual(task.name, new_task.get('name'))
            self.assertEqual(task.description, new_task.get('description'))

    def test_read_task(self):
        tasks_count = Task.objects.count()
        resp = self.client.get(reverse('list_task'))
        self.assertTrue(len(resp.context['object_list']) == tasks_count)

    def test_delete_task(self):
        tasks_count = Task.objects.count()
        task = Task.objects.get(name='TestTask')
        resp = self.client.post(reverse('task_delete', kwargs={'pk': task.id}))
        self.assertFlashMessages(resp, _('Task successfully deleted'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('list_task'))

        resp = self.client.get(reverse('list_task'))
        self.assertTrue(len(resp.context['object_list']) == tasks_count - 1)

        task = Task.objects.get(name='TestSecondTask')
        resp = self.client.post(reverse('task_delete', kwargs={'pk': task.id}))
        self.assertFlashMessages(
            resp,
            _("You can't delete this task. Only author can")
        )

    def assertFlashMessages(self, resp, message_text):
        messages = [
            message for message in map(str, get_messages(resp.wsgi_request))
        ]
        self.assertIn(message_text, messages)
