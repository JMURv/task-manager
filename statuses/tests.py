from django.test import TestCase
from django.urls import reverse
from statuses.models import Status
from users.models import User


class StatusTest(TestCase):

    def setUp(self) -> None:
        User.objects.create(
            first_name='Vladimir',
            last_name='Zhmur',
            username='jmurvv',
            email='architect.lock@outlook.com',
            password='794613825Zx'
        )
        self.user = User.objects.get(username='jmurvv')
        Status.objects.create(name='status_1')

    def test_list(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('status_list'))
        self.assertTrue(len(resp.context['object_list']) == 1)

    def test_create(self):
        self.client.force_login(self.user)
        resp = self.client.post(reverse('create_status'), {'name': 'status2'})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('status_list'))
        resp = self.client.get(reverse('status_list'))
        self.assertTrue(len(resp.context['object_list']) == 2)

    def test_update(self):
        self.client.force_login(self.user)
        tested_status = Status.objects.get(name='status_1')
        self.assertEqual(tested_status.name, 'status_1')

        resp = self.client.post(
            path=reverse('update_status', kwargs={'pk': tested_status.id}),
            data={'name': 'UpdatedName'}
        )

        self.assertEqual(resp.status_code, 302)
        tested_status.refresh_from_db()
        self.assertEqual(tested_status.name, 'UpdatedName')

    def test_DeleteStatus(self):
        self.client.force_login(self.user)
        tested_status = Status.objects.get(name='status_1')
        self.assertEqual(Status.objects.count(), 1)
        resp = self.client.post(
            path=reverse('delete_status', kwargs={'pk': tested_status.id})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Status.objects.count(), 0)
