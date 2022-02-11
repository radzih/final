# Теперь используем вместо библиотеки python-dotenv библиотеку environs

from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
PROVIDER_TOKEN = env.str("PROVIDER_TOKEN")

ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
SUPPORT = env.list("SUPPORT")
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

CHANNEL_USERNAME = env.str("CHANNEL_USERNAME")
CHANNEL_ID = env.int("CHANNEL_ID")

BOT_USERNAME = env.str("BOT_USERNAME")

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")

REDIS_HOST = env.str("REDIS_HOST")


