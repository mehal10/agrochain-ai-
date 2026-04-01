# 🌾 AgroChain AI — Smart Sustainable Farming Platform

A full-stack Django web app that connects Indian farmers, buyers, and AI to make agriculture more profitable and sustainable.

---

## ✨ Features

- **Auth system** — Register as Farmer, Buyer, Agent, or Expert
- **Farm Monitor** — Manual sensor data input (soil moisture, temperature, pH, NPK)
- **AI Chat** — Powered by Google Gemini (or OpenAI) for crop/irrigation advice
- **Marketplace** — List and buy crops directly, no middlemen
- **Analytics** — Revenue tracking and market demand forecasts
- **Smart Alerts** — Auto-generated alerts from farm data (e.g. low moisture, bad pH)
- **Subscription Plans** — Free / Pro / Enterprise tiers

---

## 🚀 Quick Start (Local)

### 1. Clone & Setup

```bash
git clone https://github.com/yourname/agrochain-ai.git
cd agrochain-ai
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY (or OPENAI_API_KEY)
```

Get a free Gemini API key at: https://aistudio.google.com/app/apikey

### 3. Run Migrations & Seed Demo Data

```bash
python manage.py migrate
python manage.py seed_demo       # Creates demo accounts
python manage.py createsuperuser # Optional: admin panel access
```

### 4. Start the Server

```bash
python manage.py runserver
```

Open: **http://127.0.0.1:8000**

**Demo credentials:**
- Farmer: `demo@agrochain.in` / `demo1234`
- Buyer: `buyer@agrochain.in` / `demo1234`

---

## 🐳 Docker Setup

```bash
cp .env.example .env
# Fill in your API keys in .env

docker-compose up --build
```

App runs at **http://localhost:8000**

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `SECRET_KEY` | Django secret key | ✅ |
| `DEBUG` | `True` for dev, `False` for prod | ✅ |
| `ALLOWED_HOSTS` | Comma-separated hostnames | ✅ |
| `LLM_PROVIDER` | `gemini` or `openai` | ✅ |
| `GEMINI_API_KEY` | Google Gemini API key (free tier) | If using Gemini |
| `OPENAI_API_KEY` | OpenAI API key | If using OpenAI |
| `AWS_ACCESS_KEY_ID` | AWS credentials for S3 media | Optional |
| `AWS_SECRET_ACCESS_KEY` | AWS secret | Optional |
| `AWS_STORAGE_BUCKET_NAME` | S3 bucket name | Optional |

---

## ☁️ Deploy to Cloud (Free Tier)

### Option A: Render (Easiest — Free Tier)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your repo
4. Set **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
5. Set **Start Command**: `gunicorn agrochain.wsgi:application`
6. Add all env variables from `.env.example`
7. Deploy!

### Option B: AWS EC2 Free Tier

```bash
# On EC2 instance (Ubuntu 22.04)
sudo apt update && sudo apt install docker.io docker-compose -y
git clone https://github.com/yourname/agrochain-ai.git
cd agrochain-ai
cp .env.example .env && nano .env   # Fill in keys
docker-compose up -d
```

### Option C: Railway

```bash
npm install -g @railway/cli
railway login
railway init
railway up
# Set env vars in Railway dashboard
```

---

## 🔄 CI/CD (GitHub Actions)

The pipeline at `.github/workflows/ci.yml` automatically:

1. **Tests** — Runs `manage.py check` and `manage.py test` on every push
2. **Builds** — Builds and pushes Docker image to Docker Hub on `main`
3. **Deploys** — Triggers deploy (configure your target in the workflow)

**GitHub Secrets needed:**
- `DOCKER_USERNAME` and `DOCKER_PASSWORD`
- `RENDER_DEPLOY_HOOK` (if using Render)
- `EC2_HOST`, `EC2_USER`, `EC2_SSH_KEY` (if using AWS EC2)

---

## 📁 Project Structure

```
agrochain-ai/
├── agrochain/              # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                   # Main app (models, views)
│   ├── models.py           # FarmerProfile, FarmData, Crop, Order, Alert
│   ├── views.py            # Page views
│   ├── admin.py
│   └── management/
│       └── commands/
│           └── seed_demo.py
├── api/                    # REST API endpoints
│   ├── views.py            # AI chat, farm data, orders
│   └── urls.py
├── templates/              # HTML templates
│   ├── base.html
│   ├── app_base.html       # Sidebar shell
│   ├── landing.html        # Auth page
│   ├── dashboard.html
│   ├── farm.html
│   ├── market.html
│   ├── analytics.html
│   ├── alerts.html
│   └── plans.html
├── static/
│   ├── css/main.css        # Full stylesheet
│   └── js/main.js          # AI chat, helpers
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
```

---

## 🤖 LLM Integration

The AI chat (`/api/ai/chat/`) supports two providers:

- **Google Gemini** (recommended, free tier): Set `LLM_PROVIDER=gemini` and `GEMINI_API_KEY`
- **OpenAI GPT-4o-mini**: Set `LLM_PROVIDER=openai` and `OPENAI_API_KEY`

If no API key is set, it falls back to a keyword-based response system so the app still works.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.0, Python 3.11 |
| Frontend | HTML5, CSS3, Vanilla JS |
| Database | SQLite (dev), PostgreSQL (prod) |
| AI | Google Gemini 2.0 Flash / OpenAI GPT-4o-mini |
| Static Files | WhiteNoise |
| Server | Gunicorn |
| Container | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Cloud | AWS EC2 / Render / Railway |

---

## 📄 License

MIT License — Free to use and modify.
