from aiogram import executor

from integrations.telegraph import TelegraphService
from loader import dp, db, bot
import middlewares, filters, handlers
from middlewares.integration import IntegrationMiddleware
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    await db.create_table_referral()
    await db.create_table_users()
    await db.create_table_support()
    await db.create_table_items()
    await db.create_table_orders()
    await db.create_table_cash()

    file_uploader = TelegraphService()
    dp.middleware.setup(IntegrationMiddleware(file_uploader))

    bot["file_uploader"] = file_uploader


    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

