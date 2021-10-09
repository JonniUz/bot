from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import CHANNELS
from keyboards.inline.subsription import check_button
from loader import dp, bot
from utils.misc.subscription import check


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    channels_format = str()
    for channel in CHANNELS:
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        channels_format += f"👉 <a href='{invite_link}'>{chat.title}</a>\n"
    await message.answer(f"Botdan foydalanish uchun quyidagilarga obuna bo'ling: \n{channels_format}",
                         reply_markup=check_button)


@dp.callback_query_handler(text="check_subs")
async def bot_start(call: types.CallbackQuery):
    result = ''
    for channel in CHANNELS:
        status = await check(user_id=call.from_user.id, channel=channel)
        chat = await bot.get_chat(channel)

        if status:
            result += f"✅ <b>{chat.title}</b> kanaliga obuna bo'lgansiz!\n\n"
        else:
            invite_link = await chat.export_invite_link()
            result += f"❌ <b>{chat.title}</b> kanaliga obuna bo'lmagansiz!" \
                      f"<a href='{invite_link}'>Obuna bo'ling</a>\n\n"
    await call.message.answer(f"{result}")
