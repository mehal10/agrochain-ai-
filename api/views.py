import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from core.models import AIConversation, FarmData, Crop, Order, Alert
from django.conf import settings


def get_llm_response(user_message: str, context: str = "") -> str:
    """Call LLM API (Gemini or OpenAI) and return text response."""
    system_prompt = """You are AgroChain AI, a smart agricultural assistant for Indian farmers.
You help with:
- Crop recommendations based on soil data
- Irrigation scheduling advice
- Market price insights
- Pest/disease identification and solutions
- Sustainable farming practices
- Weather-based farming tips
Keep responses concise, practical, and farmer-friendly. Use simple English.
Current farm context: """ + context

    provider = settings.LLM_PROVIDER

    if provider == 'openai' and settings.OPENAI_API_KEY:
        return _call_openai(system_prompt, user_message)
    elif provider == 'gemini' and settings.GEMINI_API_KEY:
        return _call_gemini(system_prompt, user_message)
    else:
        return _fallback_response(user_message)


def _call_openai(system_prompt: str, user_message: str) -> str:
    try:
        import urllib.request
        payload = json.dumps({
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 400,
        }).encode()
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
            }
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            return data['choices'][0]['message']['content']
    except Exception as e:
        return f"AI service temporarily unavailable. Error: {str(e)}"


def _call_gemini(system_prompt: str, user_message: str) -> str:
    try:
        import urllib.request
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={settings.GEMINI_API_KEY}"
        payload = json.dumps({
            "contents": [{"parts": [{"text": f"{system_prompt}\n\nUser: {user_message}"}]}],
            "generationConfig": {"maxOutputTokens": 400}
        }).encode()
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"AI service temporarily unavailable. Please check your API key. Error: {str(e)}"


def _fallback_response(msg: str) -> str:
    """Simple keyword-based fallback when no API key is set."""
    msg_lower = msg.lower()
    if any(w in msg_lower for w in ['irrigat', 'water']):
        return "💧 Based on typical soil moisture levels, irrigate your crops in the early morning (5-7 AM) to minimize evaporation. For wheat, maintain 60-70% field capacity. Set your drip irrigation for 30-45 mins per zone."
    elif any(w in msg_lower for w in ['fertiliz', 'npk', 'soil', 'nutrient']):
        return "🌱 For optimal growth, apply NPK 120:60:40 kg/ha for wheat. Use urea in split doses — 50% at sowing, 25% at tillering, 25% at heading. Add organic matter like vermicompost to improve soil health."
    elif any(w in msg_lower for w in ['price', 'market', 'sell', 'mandi']):
        return "📊 Current market insights: Wheat ₹30–35/kg (high demand), Tomato ₹22–28/kg (very high demand), Onion ₹18–22/kg (medium demand), Cotton ₹68–72/kg (high demand). Best time to sell wheat is Oct–Nov."
    elif any(w in msg_lower for w in ['pest', 'disease', 'insect', 'fungus']):
        return "🐛 Common pest alert for this season: Aphids on wheat — spray Imidacloprid 17.8 SL @ 0.3ml/L water. For fungal diseases, use Mancozeb 75 WP @ 2g/L. Maintain field hygiene and crop rotation."
    elif any(w in msg_lower for w in ['weather', 'rain', 'temperature']):
        return "🌤 For Gujarat region: Expect moderate temperatures 28–34°C. Light rainfall expected mid-month. Good conditions for sowing kharif crops. Avoid irrigation 24 hrs before expected rain."
    else:
        return "🌾 Hello! I'm AgroChain AI. I can help you with irrigation scheduling, crop recommendations, market prices, pest management, and sustainable farming practices. What would you like to know?"


@login_required
@require_http_methods(["POST"])
def ai_chat(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        # Build farm context
        latest = FarmData.objects.filter(farmer=request.user).first()
        context = ""
        if latest:
            context = f"Soil moisture: {latest.soil_moisture}%, Temp: {latest.temperature}°C, Humidity: {latest.humidity}%, pH: {latest.ph_level}"

        response_text = get_llm_response(user_message, context)

        # Save conversation
        AIConversation.objects.create(
            user=request.user,
            message=user_message,
            response=response_text
        )

        return JsonResponse({'response': response_text})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def save_farm_data(request):
    try:
        data = json.loads(request.body)
        fd = FarmData.objects.create(
            farmer=request.user,
            soil_moisture=data.get('soil_moisture', 0),
            temperature=data.get('temperature', 0),
            humidity=data.get('humidity', 0),
            ph_level=data.get('ph_level', 7),
            nitrogen=data.get('nitrogen', 0),
            phosphorus=data.get('phosphorus', 0),
            potassium=data.get('potassium', 0),
            irrigation_status=data.get('irrigation', False),
        )
        # Auto-generate alerts based on data
        if fd.soil_moisture < 30:
            Alert.objects.create(
                user=request.user,
                title='Low Soil Moisture',
                message=f'Soil moisture is at {fd.soil_moisture}%. Consider irrigating your fields.',
                severity='warning'
            )
        if fd.ph_level < 5.5 or fd.ph_level > 7.5:
            Alert.objects.create(
                user=request.user,
                title='pH Level Alert',
                message=f'Soil pH is {fd.ph_level}. Optimal range is 5.5–7.5. Consider soil amendment.',
                severity='warning'
            )
        return JsonResponse({'status': 'ok', 'id': fd.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def add_crop(request):
    try:
        data = json.loads(request.body)
        crop = Crop.objects.create(
            farmer=request.user,
            name=data['name'],
            emoji=data.get('emoji', '🌾'),
            price_per_kg=float(data['price']),
            quantity_kg=float(data['quantity']),
            quality=data.get('quality', 'Grade A'),
        )
        return JsonResponse({'status': 'ok', 'id': crop.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def place_order(request):
    try:
        data = json.loads(request.body)
        crop = Crop.objects.get(id=data['crop_id'], is_available=True)
        qty = float(data['quantity'])
        order = Order.objects.create(
            buyer=request.user,
            crop=crop,
            quantity_kg=qty,
            total_price=qty * crop.price_per_kg,
        )
        # Notify farmer
        Alert.objects.create(
            user=crop.farmer,
            title='New Order Received!',
            message=f'{request.user.get_full_name() or request.user.username} ordered {qty}kg of {crop.name} for ₹{order.total_price:.0f}',
            severity='info'
        )
        return JsonResponse({'status': 'ok', 'order_id': order.id, 'total': order.total_price})
    except Crop.DoesNotExist:
        return JsonResponse({'error': 'Crop not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def get_farm_stats(request):
    data = FarmData.objects.filter(farmer=request.user)[:30]
    return JsonResponse({
        'count': data.count(),
        'latest': {
            'soil_moisture': data[0].soil_moisture if data else 0,
            'temperature': data[0].temperature if data else 0,
            'humidity': data[0].humidity if data else 0,
            'ph_level': data[0].ph_level if data else 0,
        } if data else {}
    })
