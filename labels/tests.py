from django.test import TestCase
from users.models import User
from labels.models import Label
from django.urls import reverse


class LabelsTest(TestCase):
    def setUp(self) -> None:
        User.objects.create(
            first_name='Vladimir',
            last_name='Zhmur',
            username='jmurv',
            email='architect.lock@outlook.com',
            password='794613825Zx'
        )
        self.user = User.objects.get(username='jmurv')
        Label.objects.create(name='label_1')
        Label.objects.create(name='label_2')

    def test_list(self):
        self.client.force_login(self.user)
        resp = self.client.get(
            path=reverse('label_list')
        )
        self.assertEqual(len(resp.context['object_list']), 2)

    def test_create(self):
        self.client.force_login(self.user)
        resp = self.client.post(
            path=reverse('label_create'),
            data={'name': 'TestLabelName'}
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('label_list'))
        resp = self.client.get(
            path=reverse('label_list')
        )
        self.assertEqual(len(resp.context['object_list']), 3)

    def test_update(self):
        self.client.force_login(self.user)
        tested_label = Label.objects.get(name='label_1')
        resp = self.client.post(
            path=reverse('label_update', kwargs={'pk': tested_label.id}),
            data={'name': 'UpdateLabelName'}
        )
        self.assertEqual(resp.status_code, 302)
        tested_label.refresh_from_db()
        self.assertEqual(tested_label.name, 'UpdateLabelName')

    def test_delete(self):
        self.client.force_login(self.user)
        tested_label = Label.objects.get(name='label_1')
        self.assertEqual(Label.objects.count(), 2)
        resp = self.client.post(
            path=reverse('label_delete', kwargs={'pk': tested_label.id})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('label_list'))
        self.assertEqual(Label.objects.count(), 1)

