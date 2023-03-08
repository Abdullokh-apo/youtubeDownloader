import msilib
import os
import uuid

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentTypes
import yt_dlp

from dispatcher import dp
from state import DonwloadState


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    if message.text in ['/start', '/help']:
        await message.reply("I can help you to download videos/audios from youtube\n"
                            "To start send me link")
    await DonwloadState.url.set()


@dp.message_handler(state=DonwloadState.url)
@dp.message_handler(content_types=ContentTypes.TEXT)
async def get_link(message: types.Message, state: FSMContext):
    if message.text.startswith('https://') and 'youtube' in message.text.replace('.', ''):
        await state.update_data(url=message.text)
        menu = ReplyKeyboardMarkup(
                        keyboard=[
                            [
                                KeyboardButton(text="Video 🎥"),
                            ],
                            [
                                KeyboardButton(text="Audio 🎧")
                            ],
                        ],
                        resize_keyboard=True,
                        one_time_keyboard=True
                    )
        await message.answer('Choose file type', reply_markup=menu)
        await DonwloadState.type.set()


async def download_audio(url, f_type):
    audio_id = uuid.uuid4().fields[-1]

    try:
        if f_type == 'video':
            ydl_opts = {
                'outtmpl': f'videos/{audio_id}.mp4'
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(url)
        else:
            ydl_opts = {
                'format': 'm4a/bestaudio/best',
                'postprocessors': [{  # Extract audio using ffmpeg
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                }],
                'outtmpl': f'audio/{audio_id}.m4a'
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(url)
    except Exception:
        pass
    finally:
        return audio_id


@dp.message_handler(state=DonwloadState.type)
async def get_type(message: types.Message, state: FSMContext):
    data = await state.get_data()
    url = data['url']
    await state.finish()

    if message.text == 'Video 🎥':
        await message.answer('Video is downloading... This may take some time depending on your '
                             'internet speed')
        title = await download_audio(url, 'video')
        file_path = f'videos/{title}.mp4'

        video = open(file_path, 'rb')
        await message.answer_video(video)
        os.remove(file_path)

    elif message.text == 'Audio 🎧':
        await message.answer('Audio is downloading... This may take some time depending on your '
                             'internet speed')
        title = await download_audio(url, 'audio')
        file_path = f'audio/{title}.m4a'

        audio = open(file_path, 'rb')
        await message.answer_audio(audio)
        os.remove(file_path)

    else:
        if not message.text.startswith('https://www.youtube.com'):

            await message.answer('I can download only video and audio!')
            await get_link(message, state)


