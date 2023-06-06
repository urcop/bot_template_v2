from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.services import messages

router = Router(name='start_router')


@router.message(CommandStart)
async def start(message: Message):
    await message.answer(messages.HELLO.format(name=message.from_user.full_name))
