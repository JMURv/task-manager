from django.test import TestCase
from labels.models import Label
from django.urls import reverse
from django.contrib.auth import get_user_model


class LabelsTest(TestCase):
    fixtures = ['users.json', 'labels.json']

    def setUp(self) -> None:
        self.user = get_user_model().objects.first()
        self.client.force_login(self.user)

    def test_list(self):
        resp = self.client.get(
            path=reverse('label_list')
        )
        self.assertEqual(len(resp.context['object_list']), 2)

    def test_create(self):
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
        tested_label = Label.objects.get(name='label_1')
        resp = self.client.post(
            path=reverse('label_update', kwargs={'pk': tested_label.id}),
            data={'name': 'UpdateLabelName'}
        )
        self.assertEqual(resp.status_code, 302)
        tested_label.refresh_from_db()
        self.assertEqual(tested_label.name, 'UpdateLabelName')

    def test_delete(self):
        tested_label = Label.objects.get(name='label_1')
        self.assertEqual(Label.objects.count(), 2)
        resp = self.client.post(
            path=reverse('label_delete', kwargs={'pk': tested_label.id})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('label_list'))
        self.assertEqual(Label.objects.count(), 1)
