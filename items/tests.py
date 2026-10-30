from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import ItemReport


class ItemReportAccessTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='test-pass-123')
        self.other_user = User.objects.create_user(username='other', password='test-pass-123')
        self.item = ItemReport.objects.create(
            owner=self.owner,
            item_type=ItemReport.LOST,
            name='Notebook',
            description='Blue notebook',
            location='Library',
        )

    def test_user_cannot_edit_another_users_report(self):
        self.client.login(username='other', password='test-pass-123')
        response = self.client.post(
            reverse('edit', args=[self.item.id]),
            {
                'item_type': ItemReport.FOUND,
                'name': 'Changed',
                'description': 'Changed description',
                'location': 'Changed location',
            },
        )
        self.assertEqual(response.status_code, 404)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Notebook')

    def test_user_cannot_delete_another_users_report(self):
        self.client.login(username='other', password='test-pass-123')
        response = self.client.post(reverse('delete', args=[self.item.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(ItemReport.objects.filter(id=self.item.id).exists())

    def test_new_report_is_saved_for_logged_in_user(self):
        self.client.login(username='owner', password='test-pass-123')
        response = self.client.post(
            reverse('report'),
            {
                'item_type': ItemReport.FOUND,
                'name': 'Keys',
                'description': 'Keys with a red tag',
                'location': 'Main hall',
            },
        )
        self.assertRedirects(response, reverse('dashboard'))
        item = ItemReport.objects.get(name='Keys')
        self.assertEqual(item.owner, self.owner)

    def test_report_and_dashboard_require_login(self):
        self.assertRedirects(
            self.client.get(reverse('report')),
            '/login/?next=/report/',
        )
        self.assertRedirects(
            self.client.get(reverse('dashboard')),
            '/login/?next=/',
        )

    def test_dashboard_shows_other_reports_without_edit_controls(self):
        self.client.login(username='other', password='test-pass-123')
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'Notebook')
        self.assertNotContains(response, reverse('edit', args=[self.item.id]))
