import logging

from aiogram import Bot, Dispatcher, executor, types


# Configure logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import API_TOKEN

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
