from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FarmerProfile, FarmData, Crop, Order, Alert, AIConversation


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials')
    return redirect('landing')


def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'farmer')
        farm_name = request.POST.get('farm_name', '')
        location = request.POST.get('location', '')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('landing')

        user = User.objects.create_user(
            username=email, email=email, password=password,
            first_name=first_name, last_name=last_name
        )
        FarmerProfile.objects.create(
            user=user, role=role, farm_name=farm_name, location=location
        )
        # Seed some demo crop listings
        if role == 'farmer':
            Crop.objects.create(farmer=user, name='Wheat', emoji='🌾', price_per_kg=32, quantity_kg=500, quality='Grade A')
            Crop.objects.create(farmer=user, name='Tomato', emoji='🍅', price_per_kg=25, quantity_kg=200, quality='Grade A')

        login(request, user)
        return redirect('dashboard')
    return redirect('landing')


@login_required
def dashboard(request):
    profile = getattr(request.user, 'profile', None)
    latest_data = FarmData.objects.filter(farmer=request.user).first()
    unread_alerts = Alert.objects.filter(user=request.user, is_read=False).count()
    my_crops = Crop.objects.filter(farmer=request.user, is_available=True)
    context = {
        'profile': profile,
        'latest_data': latest_data,
        'unread_alerts': unread_alerts,
        'my_crops': my_crops,
        'page': 'dashboard',
    }
    return render(request, 'dashboard.html', context)


@login_required
def farm(request):
    if request.method == 'POST':
        FarmData.objects.create(
            farmer=request.user,
            soil_moisture=float(request.POST.get('soil_moisture', 0)),
            temperature=float(request.POST.get('temperature', 0)),
            humidity=float(request.POST.get('humidity', 0)),
            ph_level=float(request.POST.get('ph_level', 7)),
            nitrogen=float(request.POST.get('nitrogen', 0)),
            phosphorus=float(request.POST.get('phosphorus', 0)),
            potassium=float(request.POST.get('potassium', 0)),
        )
        messages.success(request, 'Farm data saved successfully!')
        return redirect('farm')

    history = FarmData.objects.filter(farmer=request.user)[:10]
    latest = history.first()
    return render(request, 'farm.html', {'history': history, 'latest': latest, 'page': 'farm'})


@login_required
def market(request):
    crops = Crop.objects.filter(is_available=True).select_related('farmer__profile')
    my_crops = Crop.objects.filter(farmer=request.user)
    return render(request, 'market.html', {'crops': crops, 'my_crops': my_crops, 'page': 'market'})


@login_required
def analytics(request):
    my_crops = Crop.objects.filter(farmer=request.user)
    orders = Order.objects.filter(buyer=request.user)
    total_revenue = sum(o.total_price for o in Order.objects.filter(crop__farmer=request.user, status='delivered'))
    return render(request, 'analytics.html', {
        'my_crops': my_crops, 'orders': orders,
        'total_revenue': total_revenue, 'page': 'analytics'
    })


@login_required
def alerts(request):
    all_alerts = Alert.objects.filter(user=request.user)
    Alert.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return render(request, 'alerts.html', {'alerts': all_alerts, 'page': 'alerts'})


@login_required
def plans(request):
    return render(request, 'plans.html', {'page': 'plans'})


@login_required
def ai_insights(request):
    from django.conf import settings
    history = AIConversation.objects.filter(user=request.user)[:10]
    return render(request, 'ai_insights.html', {
        'page': 'ai',
        'conversation_history': reversed(list(history)),
        'llm_provider': settings.LLM_PROVIDER.title(),
    })


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
