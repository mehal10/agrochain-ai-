from django.contrib import admin
from .models import FarmerProfile, FarmData, Crop, Order, Alert, AIConversation

@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'farm_name', 'location', 'farm_size']
    list_filter = ['role']

@admin.register(FarmData)
class FarmDataAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'soil_moisture', 'temperature', 'ph_level', 'recorded_at']

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'farmer', 'price_per_kg', 'quantity_kg', 'is_available']
    list_filter = ['is_available']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'crop', 'quantity_kg', 'total_price', 'status']
    list_filter = ['status']

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'severity', 'is_read', 'created_at']
    list_filter = ['severity', 'is_read']

@admin.register(AIConversation)
class AIConversationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'created_at']
