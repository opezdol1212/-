import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

TOKEN = '7916253691:AAFkjEqHvieefx71eHfMnxB4xNIjVEfFHXA'
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Настроим логирование
logging.basicConfig(level=logging.INFO)

# Текст правил
RULES_TEXT = """📘 Основные правила Великого Гэтсби

🔒 Не допускается:
Спам любого рода — будь то текст, ссылки или эмодзи без смысла.

Политика, провокации и хамство — у нас здесь уют, а не ток-шоу.

Обсуждение насилия, незаконных тем или дискриминации.

Материалы 18+, включая аватары и реакции — чату не нужен взрослый контент.

Попрошайничество — не стоит просить подарки или звать в личку без причины.

Реклама без предварительного согласования — все по договорённости с @OrvarOd.

Сбор чужих данных и их передача третьим лицам — строго запрещено.

Мошенничество в личных сообщениях, даже если собеседники — участники чата."""

# Клавиатура для группы с одной кнопкой
group_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="ПРАВИЛА", url="https://t.me/rules2310_bot")]
])

# Клавиатура для личных сообщений с кнопкой "ПРАВИЛА"
user_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="ПРАВИЛА", callback_data="show_rules")]
])

async def send_rules_reminder():
    while True:
        try:
            await bot.send_message(chat_id='-1002596135103', text="Не забудьте о правилах!",
                                   reply_markup=group_keyboard)
            logging.info("Напоминание отправлено.")
        except Exception as e:
            logging.error(f"Ошибка при отправке напоминания: {e}")
        await asyncio.sleep(1800)

@dp.callback_query(lambda c: c.data == "show_rules")
async def show_rules(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(chat_id=callback_query.from_user.id, text=RULES_TEXT)

@dp.message()
async def get_chat_id(message: types.Message):
    logging.info(f"Received message from {message.chat.id} of type {message.chat.type}: {message.text}")

    if message.chat.type in ['group', 'supergroup']:
        await message.reply("Чтобы ознакомиться с правилами или перейти в чат с ботом, нажмите кнопку ниже:",
                            reply_markup=group_keyboard)
    else:
        await message.reply("Чтобы ознакомиться с правилами, нажмите кнопку ниже:", reply_markup=user_keyboard)

async def main():
    asyncio.create_task(send_rules_reminder())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
