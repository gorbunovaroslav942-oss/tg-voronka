import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Берем данные из настроек сервера (Environment Variables)
TOKEN = os.getenv("BOT_TOKEN")
# ID твоих каналов (подставь свои цифры)
CHANNEL_1_ID = -1002047321568 
CHANNEL_2_ID = -1002145678910
# Твой ID для админки
ADMIN_ID = 1256583707

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def check_subscription(user_id):
    """Проверка, подписан ли юзер на оба канала"""
    for chat_id in [CHANNEL_1_ID, CHANNEL_2_ID]:
        try:
            member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            if member.status in ["left", "kicked"]:
                return False
        except Exception as e:
            logging.error(f"Ошибка проверки {chat_id}: {e}")
            return False
    return True

def get_keyboard():
    """Клавиатура с кнопками подписки"""
    buttons = [
        [InlineKeyboardButton(text="1️⃣ Подписаться на Канал 1", url=URL_1)],
        [InlineKeyboardButton(text="2️⃣ Подписаться на Канал 2", url=URL_2)],
        [InlineKeyboardButton(text="✅ Проверить подписку", callback_data="verify")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if await check_subscription(message.from_user.id):
        await message.answer(f"✅ Доступ открыт! Твоя ссылка в приватный канал:\n{PRIVATE_URL}")
    else:
        await message.answer(
            "👋 Привет! Чтобы попасть в приватный канал, нужно выполнить 2 простых действия:\n\n"
            "1. Подпишись на оба канала ниже\n"
            "2. Нажми кнопку проверки",
            reply_markup=get_keyboard()
        )

@dp.callback_query(F.data == "verify")
async def check_callback(callback: types.CallbackQuery):
    if await check_subscription(callback.from_user.id):
        await callback.message.edit_text(
            f"🎉 Поздравляем! Ты в деле.\n\nСсылка на основной канал:\n{PRIVATE_URL}",
            reply_markup=None
        )
    else:
        await callback.answer("❌ Ты подписался не на все каналы!", show_alert=True)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
