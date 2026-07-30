# 🌦️ Telegram Weather Bot

[![CI](https://github.com/Tymur-z/Telegam_weather_bot/actions/workflows/ci.yml/badge.svg)](https://github.com/Tymur-z/Telegam_weather_bot/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

A fully working Telegram weather bot written in Python with [aiogram 3](https://docs.aiogram.dev/).
It shows current weather and a 5-day forecast, supports geolocation, favorite cities,
and switching between metric and imperial units.

**100% free to run** — see [Free API key](#-free-api-key-no-credit-card) below.

## ✨ Features

- 🌤️ Current weather by city name (or just type a city name directly)
- 📅 5-day forecast
- 📍 Weather by location (tap "Send location")
- ⭐ Favorite cities for quick access
- ⚙️ Switch units: °C / m/s ↔ °F / mph
- 💬 Clean menu with reply and inline keyboards
- 🗄️ Per-user data stored in SQLite (aiosqlite)
- 🧩 Modular structure (handlers / keyboards / services / database / states / utils)
- ✅ Unit tests + GitHub Actions CI

## 🆓 Free API key, no credit card

This bot uses OpenWeatherMap's **Current Weather Data** and **5 Day / 3 Hour Forecast**
endpoints (`/data/2.5/weather` and `/data/2.5/forecast`). These are part of OpenWeatherMap's
permanent free tier:

- Up to 60 calls/minute and 1,000,000 calls/month
- More than enough for a personal or small public bot

> ⚠️ Note: OpenWeatherMap also sells a separate product called "One Call API 3.0 / 4.0"
> which requires a subscription after a small daily allowance. This project does **not**
> use that endpoint, so you will not be charged anything by following the setup below.

## 🗂️ Project structure

```
weather-telegram-bot/
├── main.py                    # Entry point: starts the bot
├── config.py                  # Loads environment variables
├── requirements.txt           # Runtime dependencies
├── requirements-dev.txt       # + testing/linting tools
├── pytest.ini
├── .env.example                # Template for your own .env file
├── .github/workflows/ci.yml    # Lint + test on every push/PR
├── database/
│   └── db.py                   # SQLite: users, favorite cities
├── handlers/
│   ├── start.py                 # /start, /help
│   ├── weather.py               # Current weather / forecast / location
│   ├── favorites.py             # Favorite cities
│   └── settings.py              # Units settings
├── keyboards/
│   └── keyboards.py            # Reply & inline keyboards
├── services/
│   └── weather_api.py          # OpenWeatherMap API client
├── states/
│   └── states.py                # aiogram FSM states
├── utils/
│   └── formatting.py           # Turns API responses into nice messages
└── tests/
    └── test_formatting.py      # Unit tests (no network needed)
```

## 🚀 Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/weather-telegram-bot.git
cd weather-telegram-bot
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get a Telegram bot token (free)

1. Open [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow the prompts
3. Copy the token it gives you

### 5. Get an OpenWeatherMap API key (free, no card)

1. Create a free account at [openweathermap.org/api](https://openweathermap.org/api)
2. Copy your API key from the dashboard
3. New keys can take up to ~2 hours to activate — if you get an error immediately after
   signing up, just wait a bit and try again

### 6. Configure environment variables

```bash
cp .env.example .env
```

Then edit `.env`:

```
BOT_TOKEN=your_bot_token_here
OWM_API_KEY=your_openweathermap_key_here
```

### 7. Run the bot

```bash
python main.py
```

Find your bot on Telegram and send `/start`.

## 🧪 Running tests

```bash
pip install -r requirements-dev.txt
pytest
ruff check .
```

## 🛠️ Tech stack

- [Python 3.10+](https://www.python.org/)
- [aiogram 3](https://docs.aiogram.dev/) — async Telegram bot framework
- [aiohttp](https://docs.aiohttp.org/) — async HTTP client for the weather API
- [aiosqlite](https://github.com/omnilib/aiosqlite) — async SQLite
- [OpenWeatherMap API](https://openweathermap.org/api) — weather data (free tier)
- [python-dotenv](https://github.com/theskumar/python-dotenv) — environment variables
- [pytest](https://docs.pytest.org/) + [ruff](https://docs.astral.sh/ruff/) — tests & linting

## 🤝 Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

Released under the [MIT License](LICENSE) — free to use, modify, and share.

## 💡 Ideas for extending this project

- Scheduled weather alerts (APScheduler)
- Multi-language support
- Hourly temperature charts (matplotlib / QuickChart)
- Docker support and cloud deployment
