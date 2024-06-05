import googletrans
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from googletrans import Translator

translator = Translator()
languages = googletrans.LANGUAGES
languages_list = list(languages.values())
capitalize_languages_list = []
for i in languages_list:
    capitalize_languages_list.append(i.capitalize())

def main_menu():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    rkm.row(KeyboardButton("Wikipedia"), KeyboardButton("Instagram downloader"), KeyboardButton("YouTube downloader"))
    rkm.row(KeyboardButton("Valuta kursi"), KeyboardButton("Translator"), KeyboardButton("Photo to pdf"))
    rkm.row(KeyboardButton('The phone will find the Username of the user from the number'))
    return rkm


def value():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    rkm.row(KeyboardButton("Valyutani kiriting"))
    rkm.row(KeyboardButton("BACK TO MENU"))
    return rkm


def kurs():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    rkm.row(KeyboardButton('usd$'), KeyboardButton('uzs🇺🇿'), KeyboardButton('eur¥'), KeyboardButton('gpb£'))
    rkm.row(KeyboardButton('cad🇨🇦'), KeyboardButton('sud🇸🇩'), KeyboardButton('rub₽'), KeyboardButton('en€'))
    rkm.row(KeyboardButton('BACK TO MENU'))
    return rkm


def back():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    rkm.row(KeyboardButton('BACK TO MENU'))
    return rkm


def lang():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    for e in capitalize_languages_list:
        rkm.row(KeyboardButton(e))
    rkm.row(KeyboardButton("BACK TO MENU"))
    return rkm
