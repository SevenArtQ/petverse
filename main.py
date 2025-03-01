from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import json
import os
import asyncio
from datetime import datetime
from pet_manager import PetManager
from bot_config import BOT_TOKEN, WEBAPP_URL

# Конфигурация
TOKEN = "7631766370:AAF4mf7nrDIKBDCwNpRMupADnXvoyixP0R4"

# Структура для хранения данных питомцев
class Pet:
    def __init__(self, owner_id, name=None):
        self.owner_id = owner_id
        self.name = name
        self.type = "egg"  # начинаем с яйца
        self.hunger = 100
        self.happiness = 100
        self.last_feed = datetime.now().timestamp()
        self.experience = 0
        self.level = 1

class PetVerseBot:
    def __init__(self):
        self.pets = {}  # словарь для хранения питомцев
        self.load_data()
        self.pet_manager = PetManager()

    async def start(self, update: Update, context):
        keyboard = [[InlineKeyboardButton("🎮 Открыть PetVerse", web_app=WebAppInfo(url=WEBAPP_URL))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Привет! Нажми кнопку ниже, чтобы открыть PetVerse:",
            reply_markup=reply_markup
        )

    async def name_pet(self, update: Update, context):
        user_id = update.effective_user.id
        if user_id not in self.pets:
            await update.message.reply_text("Сначала получите питомца через /start")
            return

        if not context.args:
            await update.message.reply_text("Использование: /name <имя>")
            return

        name = " ".join(context.args)
        self.pets[user_id].name = name
        await update.message.reply_text(f"Отлично! Ваш питомец теперь называется {name}! 🎉")

    def load_data(self):
        if os.path.exists('pets_data.json'):
            with open('pets_data.json', 'r') as f:
                data = json.load(f)
                for user_id, pet_data in data.items():
                    pet = Pet(int(user_id))
                    pet.__dict__.update(pet_data)
                    self.pets[int(user_id)] = pet

    def save_data(self):
        data = {str(user_id): pet.__dict__ for user_id, pet in self.pets.items()}
        with open('pets_data.json', 'w') as f:
            json.dump(data, f)

    async def status(self, update: Update, context):
        user_id = update.effective_user.id
        if user_id not in self.pets:
            await update.message.reply_text("У вас нет питомца! Используйте /start чтобы получить его.")
            return

        pet = self.pets[user_id]
        pet = self.pet_manager.calculate_stats(pet)
        
        status_text = (
            f"🐾 Питомец: {pet.name or 'Без имени'}\n"
            f"📊 Уровень: {pet.level}\n"
            f"⭐ Опыт: {pet.experience}/{pet.level * 100}\n"
            f"🍖 Голод: {pet.hunger:.1f}%\n"
            f"😊 Счастье: {pet.happiness:.1f}%\n"
            f"🥚 Тип: {pet.type}"
        )
        await update.message.reply_text(status_text)

    async def feed(self, update: Update, context):
        user_id = update.effective_user.id
        if user_id not in self.pets:
            await update.message.reply_text("У вас нет питомца! Используйте /start чтобы получить его.")
            return

        pet = self.pets[user_id]
        success, message = self.pet_manager.feed_pet(pet)
        await update.message.reply_text(message)
        
        # Проверяем повышение уровня
        leveled_up, level_message = self.pet_manager.check_level_up(pet)
        if leveled_up:
            await update.message.reply_text(level_message)
        
        self.save_data()

    async def play(self, update: Update, context):
        user_id = update.effective_user.id
        if user_id not in self.pets:
            await update.message.reply_text("У вас нет питомца! Используйте /start чтобы получить его.")
            return

        pet = self.pets[user_id]
        success, message = self.pet_manager.play_with_pet(pet)
        await update.message.reply_text(message)
        
        # Проверяем повышение уровня
        leveled_up, level_message = self.pet_manager.check_level_up(pet)
        if leveled_up:
            await update.message.reply_text(level_message)
        
        self.save_data()

def run_bot():
    bot = PetVerseBot()
    application = Application.builder().token(TOKEN).build()
    
    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("name", bot.name_pet))
    application.add_handler(CommandHandler("status", bot.status))
    application.add_handler(CommandHandler("feed", bot.feed))
    application.add_handler(CommandHandler("play", bot.play))
    
    print("Бот запущен...")
    application.run_polling()
    print("\nБот остановлен...")

if __name__ == "__main__":
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\nБот остановлен по команде пользователя...") 