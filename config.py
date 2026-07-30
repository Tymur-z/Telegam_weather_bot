import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWM_API_KEY = os.getenv("OWM_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing. Copy .env.example to .env and fill it in.")
if not OWM_API_KEY:
    raise ValueError("OWM_API_KEY is missing. Copy .env.example to .env and fill it in.")

DB_PATH = os.getenv("DB_PATH", "weather_bot.db")
DEFAULT_UNITS = "metric"
