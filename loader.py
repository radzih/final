from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from data import config
from utils.db_api.postgresql import Database

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
db = Database()
storage = RedisStorage2(host=config.REDIS_HOST)
dp = Dispatcher(bot, storage=storage)

