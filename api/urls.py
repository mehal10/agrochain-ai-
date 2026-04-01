from django.urls import path
from . import views

urlpatterns = [
    path('ai/chat/', views.ai_chat, name='ai_chat'),
    path('farm/save/', views.save_farm_data, name='save_farm_data'),
    path('farm/stats/', views.get_farm_stats, name='farm_stats'),
    path('crop/add/', views.add_crop, name='add_crop'),
    path('order/place/', views.place_order, name='place_order'),
]
