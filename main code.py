import os
import aiohttp
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from dotenv import load_dotenv


# Загружаем токены из .env
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN1")
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

async def get_weather(city: str):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric", "lang": "ru"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                desc = data["weather"][0]["description"].capitalize()
                temp = data["main"]["temp"]
                feels = data["main"]["feels_like"]
                humidity = data["main"]["humidity"]
                return f"Погода в {city}:\n{desc}\nТемпература: {temp}°C (ощущается как {feels}°C)\nВлажность: {humidity}%"
            else:
                return "Не удалось получить данные о погоде. Проверьте название города."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь мне название города, и я покажу текущую погоду 🌦"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text.strip()
    weather_info = await get_weather(city)
    await update.message.reply_text(weather_info)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()
