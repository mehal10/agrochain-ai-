from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import FarmerProfile, FarmData, Crop, Alert
import json


class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_landing_page_loads(self):
        resp = self.client.get(reverse('landing'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'AgroChain')

    def test_register_creates_user(self):
        resp = self.client.post(reverse('register'), {
            'first_name': 'Ravi', 'last_name': 'Patel',
            'email': 'ravi@test.in', 'password': 'testpass123',
            'role': 'farmer', 'farm_name': 'Test Farm', 'location': 'Gujarat'
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(username='ravi@test.in').exists())
        profile = FarmerProfile.objects.get(user__username='ravi@test.in')
        self.assertEqual(profile.role, 'farmer')
        self.assertEqual(profile.farm_name, 'Test Farm')

    def test_login_redirects_to_dashboard(self):
        User.objects.create_user(username='u@test.in', password='pass123')
        resp = self.client.post(reverse('login'), {'username': 'u@test.in', 'password': 'pass123'})
        self.assertRedirects(resp, reverse('dashboard'))

    def test_bad_login_stays_on_landing(self):
        resp = self.client.post(reverse('login'), {'username': 'bad@test.in', 'password': 'wrong'})
        self.assertRedirects(resp, reverse('landing'))

    def test_dashboard_requires_login(self):
        resp = self.client.get(reverse('dashboard'))
        self.assertRedirects(resp, '/?next=/dashboard/')


class DashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='farmer@test.in', password='pass123', first_name='Test')
        FarmerProfile.objects.create(user=self.user, role='farmer')
        self.client.login(username='farmer@test.in', password='pass123')

    def test_dashboard_loads(self):
        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 200)

    def test_farm_page_loads(self):
        resp = self.client.get(reverse('farm'))
        self.assertEqual(resp.status_code, 200)

    def test_market_page_loads(self):
        resp = self.client.get(reverse('market'))
        self.assertEqual(resp.status_code, 200)

    def test_analytics_page_loads(self):
        resp = self.client.get(reverse('analytics'))
        self.assertEqual(resp.status_code, 200)

    def test_alerts_page_loads(self):
        resp = self.client.get(reverse('alerts'))
        self.assertEqual(resp.status_code, 200)

    def test_plans_page_loads(self):
        resp = self.client.get(reverse('plans'))
        self.assertEqual(resp.status_code, 200)


class APITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='api@test.in', password='pass123')
        FarmerProfile.objects.create(user=self.user, role='farmer')
        self.client.login(username='api@test.in', password='pass123')

    def _post_json(self, url, data):
        return self.client.post(
            url, json.dumps(data),
            content_type='application/json',
            HTTP_X_CSRFTOKEN='test'
        )

    def test_save_farm_data(self):
        resp = self._post_json('/api/farm/save/', {
            'soil_moisture': 65, 'temperature': 28, 'humidity': 70,
            'ph_level': 6.5, 'nitrogen': 120, 'phosphorus': 60,
            'potassium': 40, 'irrigation': True
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['status'], 'ok')
        self.assertTrue(FarmData.objects.filter(farmer=self.user).exists())

    def test_save_farm_data_generates_alert_on_low_moisture(self):
        self._post_json('/api/farm/save/', {
            'soil_moisture': 20, 'temperature': 28, 'humidity': 60,
            'ph_level': 6.8, 'nitrogen': 80, 'phosphorus': 40, 'potassium': 30
        })
        self.assertTrue(Alert.objects.filter(user=self.user, title='Low Soil Moisture').exists())

    def test_add_crop(self):
        resp = self._post_json('/api/crop/add/', {
            'name': 'Wheat', 'emoji': '🌾', 'price': 32, 'quantity': 500, 'quality': 'Grade A'
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['status'], 'ok')
        self.assertTrue(Crop.objects.filter(farmer=self.user, name='Wheat').exists())

    def test_place_order(self):
        seller = User.objects.create_user(username='seller@test.in', password='pass123')
        crop = Crop.objects.create(farmer=seller, name='Tomato', emoji='🍅', price_per_kg=25, quantity_kg=200)
        resp = self._post_json('/api/order/place/', {'crop_id': crop.id, 'quantity': 10})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['status'], 'ok')
        self.assertAlmostEqual(data['total'], 250.0)

    def test_ai_chat_returns_response(self):
        resp = self._post_json('/api/ai/chat/', {'message': 'When should I irrigate wheat?'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('response', data)
        self.assertGreater(len(data['response']), 10)

    def test_ai_chat_empty_message_returns_400(self):
        resp = self._post_json('/api/ai/chat/', {'message': ''})
        self.assertEqual(resp.status_code, 400)

    def test_get_farm_stats(self):
        FarmData.objects.create(farmer=self.user, soil_moisture=72, temperature=28, humidity=65, ph_level=6.8)
        resp = self.client.get('/api/farm/stats/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('latest', data)
        self.assertEqual(data['latest']['soil_moisture'], 72)

    def test_api_requires_login(self):
        self.client.logout()
        resp = self._post_json('/api/ai/chat/', {'message': 'hello'})
        self.assertEqual(resp.status_code, 302)
