from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('farmer', 'Farmer'), ('buyer', 'Buyer'), ('agent', 'Agent'), ('expert', 'Expert')], default='farmer', max_length=20)),
                ('farm_name', models.CharField(blank=True, max_length=100)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('farm_size', models.FloatField(default=0, help_text='in acres')),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='FarmData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soil_moisture', models.FloatField(default=0)),
                ('temperature', models.FloatField(default=0)),
                ('humidity', models.FloatField(default=0)),
                ('ph_level', models.FloatField(default=7.0)),
                ('nitrogen', models.FloatField(default=0)),
                ('phosphorus', models.FloatField(default=0)),
                ('potassium', models.FloatField(default=0)),
                ('irrigation_status', models.BooleanField(default=False)),
                ('recorded_at', models.DateTimeField(auto_now_add=True)),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='farm_data', to='auth.user')),
            ],
            options={'ordering': ['-recorded_at']},
        ),
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('emoji', models.CharField(default='🌾', max_length=10)),
                ('price_per_kg', models.FloatField()),
                ('quantity_kg', models.FloatField()),
                ('quality', models.CharField(default='Grade A', max_length=50)),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crops', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_kg', models.FloatField()),
                ('total_price', models.FloatField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='auth.user')),
                ('crop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.crop')),
            ],
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('severity', models.CharField(choices=[('info', 'Info'), ('warning', 'Warning'), ('critical', 'Critical')], default='info', max_length=20)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='farm_alerts', to='auth.user')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='AIConversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('response', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ai_conversations', to='auth.user')),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
