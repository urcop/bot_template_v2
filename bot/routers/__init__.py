from aiogram import Dispatcher

from . import start


def setup(dp: Dispatcher):
    dp.include_router(start.router)
