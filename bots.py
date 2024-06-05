import logging
import os

import requests
import wikipedia
from PIL import Image
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile
from fpdf import FPDF
from googletrans import Translator
from pytube import YouTube

from keyboard import value, kurs, back, main_menu, lang
from state import Value, File, Wiki, Download_yt, Trans, Tel

storage = MemoryStorage()
BOT_TOKEN = "7069079864:AAHsw_FvbneRiBx4AjV_kRSfpGOCESb1p-A"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)

API_KEY = "5bbf3606ce5e654dde3a5530"
translator = Translator()
wikipedia.set_lang("uz")
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(Text(equals='Photo to pdf'), state=None)
async def start_bot(message: types.Message, state: FSMContext):
    await message.answer("rasmlar tashla", reply_markup=back())
    await File.out.set()


@dp.message_handler(state=File.out, content_types=['photo'])
async def handle_docs_photo(message: types.Message, state: FSMContext):
    try:
        photo = message.photo[-1]
        photo_path = f"photos/{photo.file_id}.jpg"

        # Make sure directories exist
        if not os.path.exists('photos'):
            os.makedirs('photos')
        if not os.path.exists('pdfs'):
            os.makedirs('pdfs')

        # Download photo
        await photo.download(destination_file=photo_path)

        pdf_path = f"pdfs/{photo.file_id}.pdf"

        # Convert the image to PDF
        image = Image.open(photo_path)
        pdf = FPDF()
        pdf.add_page()
        pdf.image(photo_path, x=10, y=10, w=190)
        pdf.output(pdf_path, "F")

        # Send the PDF to the user
        await message.reply_document(InputFile(pdf_path),
                                     caption="____________________________________\nPowered by @minecraft_top_games")

        # Clean up the files
        os.remove(photo_path)
        os.remove(pdf_path)

    except Exception as e:
        logging.error(f"Error handling photo: {e}")
        await message.reply("Rasmni PDF faylga aylantirishda xatolik yuz berdi.")
    await state.finish()


@dp.message_handler(commands="start")
async def start_bot(messege: types.Message):
    await messege.answer("Botga xush kelibsan ukam", reply_markup=main_menu())


@dp.message_handler(Text(equals="Valuta kursi"))
async def start_bot(message: types.Message):
    await message.answer("Salom, valyutani tanlsh", reply_markup=value())


@dp.message_handler(Text(equals="Valyutani kiriting"), state=None)
async def start_bot(message: types.Message):
    await message.answer("1 valyutani tanlang", reply_markup=kurs())
    await Value.value.set()


@dp.message_handler(state=Value.value)
async def start_bot(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'uzs🇺🇿':
            data["first"] = 'uzs'
        elif message.text == 'usd$':
            data["first"] = 'usd'
        elif message.text == 'eur¥':
            data["first"] = 'eur'
        elif message.text == 'gpb£':
            data["first"] = 'gpb'
        elif message.text == 'cad🇨🇦':
            data["first"] = 'cad'
        elif message.text == 'sud🇸🇩':
            data["first"] = 'sud'
        elif message.text == 'rub₽':
            data["first"] = 'rub'
        elif message.text == 'en€':
            data["first"] = 'en'
    await message.answer("2 valyutani tanlang", reply_markup=kurs())
    await Value.next()


@dp.message_handler(state=Value.kurs)
async def start_bot(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'uzs🇺🇿':
            data["second"] = 'uzs'
        elif message.text == 'usd$':
            data["second"] = 'usd'
        elif message.text == 'eur¥':
            data["second"] = 'eur'
        elif message.text == 'gpb£':
            data["second"] = 'gpb'
        elif message.text == 'cad🇨🇦':
            data["second"] = 'cad'
        elif message.text == 'sud🇸🇩':
            data["second"] = 'sud'
        elif message.text == 'rub₽':
            data["second"] = 'rub'
        elif message.text == 'en€':
            data["second"] = 'en'
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{data['first']}/{data['second']}"
        result = requests.get(url)
        kurs = result.json()["conversion_rate"]
        await message.answer(
            f"bungungi {data['first']}ning narxi {data['second']}da: {kurs}\n____________________________________\n"
            f"Powered by @minecraft_top_games", reply_markup=back())
        await state.finish()


@dp.message_handler(Text(equals='BACK TO MENU'))
async def start_bot(message: types.Message, state: FSMContext):
    await message.answer("Main Menu", reply_markup=main_menu())
    await state.finish()


@dp.message_handler(Text(equals='BACK TO MENU'), state=Download_yt.loop)
async def start_bot(message: types.Message, state: FSMContext):
    await message.answer("Main Menu", reply_markup=main_menu())
    await state.finish()


@dp.message_handler(Text(equals='Wikipedia'), state=None)
async def start_wiki(message: types.Message):
    await message.answer("Wikipedia bot ishga tushdi", reply_markup=back())
    await Wiki.loop.set()


@dp.message_handler(state=Wiki.loop)
async def echo(message: types.Message, state: FSMContext):
    if message.text != "BACK TO MENU":
        result = wikipedia.summary(message.text)
        await message.answer(f"{result} \n____________________________________\nPowered by @minecraft_top_games",
                             reply_markup=back())
    else:
        await state.finish()


@dp.message_handler(Text(equals="YouTube downloader"))
async def send_welcome(message: types.Message):
    await message.reply("Salom! Menga YouTube video havolasini yuboring va men uni siz uchun yuklab beraman.",
                        reply_markup=back())
    await Download_yt.loop.set()


@dp.message_handler(Text(equals="The phone will find the Username of the user from the number"), state=None)
async def send_welcome(message: types.Message):
    await message.reply("Salom! Menga raqam yuboring va men uni @username tashlab beraman.",
                        reply_markup=back())
    await Tel.loop.set()


@dp.message_handler(state=Tel.loop)
async def download_youtube_video(message: types.Message, state: FSMContext):
    username = message.text
    if message.text != "BACK TO MENU":
        await state.finish()
    elif username.startswith("+"):
        if len(username) == 13:
            await message.reply(f"https://t.me/{username}")
        else:
            await message.answer("Raqam xato kiritilgan")
    await Tel.loop.set()


@dp.message_handler(Text(startswith='https://youtu'), state=Download_yt.loop)
async def download_youtube_video(message: types.Message):
    url = message.text
    await message.reply("Videoni yuklab olmoqdaman, biroz kuting...")

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video_path = stream.download()
        await message.reply_video(video=open(video_path, 'rb'), caption="Powered by @minecraft_top_games")
        os.remove(video_path)
    except Exception as e:
        await message.reply(f"Xatolik yuz berdi: {str(e)}")


@dp.message_handler(Text(equals="Translator"))
async def send_welcome(message: types.Message, state: FSMContext):
    if message.text != "BACK TO MENU":
        await message.reply("Tilni tanlang", reply_markup=lang())
        await Trans.loop.set()
    else:
        await state.finish()


@dp.message_handler(state=Trans.loop)
async def translate_message(message: types.Message, state: FSMContext):
    if message.text != "BACK TO MENU":
        async with state.proxy() as data:
            data['lang'] = message.text
            await message.answer("Til tanlandi")
        await Trans.next()
    else:
        await state.finish()


@dp.message_handler(state=Trans.lang)
async def translated(message: types.Message, state: FSMContext):
    if message.text != "BACK TO MENU":
        async with state.proxy() as data:
            translated_text = translator.translate(message.text, dest=data['lang']).text
            await message.reply(translated_text)
        await Trans.loop.set()
    else:
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
