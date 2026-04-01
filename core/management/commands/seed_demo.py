from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import FarmerProfile, FarmData, Crop, Alert


class Command(BaseCommand):
    help = 'Seed demo data for AgroChain AI'

    def handle(self, *args, **kwargs):
        # Create demo farmer
        if not User.objects.filter(username='demo@agrochain.in').exists():
            user = User.objects.create_user(
                username='demo@agrochain.in',
                email='demo@agrochain.in',
                password='demo1234',
                first_name='Ravi',
                last_name='Patel'
            )
            FarmerProfile.objects.create(
                user=user, role='farmer',
                farm_name='Green Valley Farm',
                location='Anand, Gujarat',
                farm_size=12.5
            )
            FarmData.objects.create(
                farmer=user, soil_moisture=72, temperature=28,
                humidity=65, ph_level=6.8, nitrogen=120,
                phosphorus=60, potassium=40, irrigation_status=True
            )
            Crop.objects.create(farmer=user, name='Wheat', emoji='🌾', price_per_kg=32, quantity_kg=500, quality='Grade A')
            Crop.objects.create(farmer=user, name='Tomato', emoji='🍅', price_per_kg=25, quantity_kg=200, quality='Organic')
            Crop.objects.create(farmer=user, name='Cotton', emoji='🌸', price_per_kg=70, quantity_kg=300, quality='Grade A')
            Alert.objects.create(user=user, title='Welcome to AgroChain AI!', message='Your farm account is ready. Start by adding your farm sensor data.', severity='info')
            self.stdout.write(self.style.SUCCESS('✅ Demo farmer created: demo@agrochain.in / demo1234'))
        else:
            self.stdout.write('Demo farmer already exists.')

        # Create demo buyer
        if not User.objects.filter(username='buyer@agrochain.in').exists():
            buyer = User.objects.create_user(
                username='buyer@agrochain.in',
                email='buyer@agrochain.in',
                password='demo1234',
                first_name='Amit',
                last_name='Kapoor'
            )
            FarmerProfile.objects.create(user=buyer, role='buyer', location='Ahmedabad, Gujarat')
            self.stdout.write(self.style.SUCCESS('✅ Demo buyer created: buyer@agrochain.in / demo1234'))
        else:
            self.stdout.write('Demo buyer already exists.')

        self.stdout.write(self.style.SUCCESS('🌾 Seed complete!'))
