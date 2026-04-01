from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.landing, name='landing'),
    path('dashboard/', core_views.dashboard, name='dashboard'),
    path('farm/', core_views.farm, name='farm'),
    path('market/', core_views.market, name='market'),
    path('analytics/', core_views.analytics, name='analytics'),
    path('alerts/', core_views.alerts, name='alerts'),
    path('plans/', core_views.plans, name='plans'),
    path('ai/', core_views.ai_insights, name='ai_insights'),
    path('login/', core_views.login_view, name='login'),
    path('register/', core_views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('api/', include('api.urls')),
]

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'
