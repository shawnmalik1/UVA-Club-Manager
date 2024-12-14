from django.test import TestCase
from django.test import SimpleTestCase
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import CheckIn, Club, Event
from django.test import Client
from .models import Profile
from datetime import date

### Testing common user views
class TestViews_Common(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user)
        client = Client()

    def test_view_calendar_member(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('calendar'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar.html')

    def test_files(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('file_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'file_list.html')

    def test_chat(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('chat_room'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat_room.html')


    def test_suggestion_box(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('suggestion_box'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'suggestion_box.html')

### Testing administrator views
class TestViews_PMA(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user)
        client = Client()

    def test_view_calendar_admin(self):
        self.profile.is_pma_administrator = True
        self.profile.save()

        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('calendar'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_non_admin.html')

    def test_view_suggestion(self):
        self.profile.is_pma_administrator = True
        self.profile.save()

        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('suggestion_box'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'suggestion_list.html')

    def test_view_file_admin(self):
        self.profile.is_pma_administrator = True
        self.profile.save()

        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('file_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'file_list.html')

### Testing add event feature on calendar
class TestCalendar(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

    def test_add_event_with_current_date(self):
        current_date = date.today().strftime('%Y-%m-%d')
        # Event data with the current date
        event_data = {
            'title': 'Test Event Today',
            'date': current_date,
            'description': 'This is a test event for today.'
        }

        response = self.client.post(reverse('add_event'), data=event_data)
        self.assertEqual(response.status_code, 302)  # Redirect to calendar page
        self.assertTrue(Event.objects.filter(title='Test Event Today', date=current_date).exists())

        event = Event.objects.get(title='Test Event Today', date=current_date)
        self.assertEqual(event.description, 'This is a test event for today.')
        self.assertEqual(event.user, self.user)

