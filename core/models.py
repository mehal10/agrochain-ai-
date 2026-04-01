from django.db import models
from django.contrib.auth.models import User


class FarmerProfile(models.Model):
    ROLE_CHOICES = [('farmer', 'Farmer'), ('buyer', 'Buyer'), ('agent', 'Agent'), ('expert', 'Expert')]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='farmer')
    farm_name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    farm_size = models.FloatField(default=0, help_text='in acres')
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.role})"


class FarmData(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farm_data')
    soil_moisture = models.FloatField(default=0)
    temperature = models.FloatField(default=0)
    humidity = models.FloatField(default=0)
    ph_level = models.FloatField(default=7.0)
    nitrogen = models.FloatField(default=0)
    phosphorus = models.FloatField(default=0)
    potassium = models.FloatField(default=0)
    irrigation_status = models.BooleanField(default=False)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"FarmData for {self.farmer.username} at {self.recorded_at}"


class Crop(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crops')
    name = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10, default='🌾')
    price_per_kg = models.FloatField()
    quantity_kg = models.FloatField()
    quality = models.CharField(max_length=50, default='Grade A')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.farmer.username}"


class Order(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('confirmed', 'Confirmed'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')]
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity_kg = models.FloatField()
    total_price = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.buyer.username}"


class Alert(models.Model):
    SEVERITY_CHOICES = [('info', 'Info'), ('warning', 'Warning'), ('critical', 'Critical')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farm_alerts')
    title = models.CharField(max_length=200)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.severity}] {self.title}"


class AIConversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_conversations')
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
