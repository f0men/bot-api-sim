import os

import telebot
from telebot import types
from dotenv import load_dotenv

dirname = os.path.dirname(__file__) # сохрнение название директори текущего файла
dotenv_path = os.path.join(dirname, '.env') # сохранение директории env-файла
load_dotenv(dotenv_path) # загрузка данных env-файла

TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(TOKEN)


user_state = {}  # Глобальная переменная для отслеживания состояния пользователя

@bot.message_handler(commands=['start'])
def start(message):
    user_state[message.chat.id] = 'main_menu'  # Установка состояния пользователю
    markup = types.ReplyKeyboardMarkup()
    button_1 = types.KeyboardButton('Перейти в Google sheets')
    button_2 = types.KeyboardButton('Отобразить графики в чате')
    button_3 = types.KeyboardButton('Получить данные в формате txt')
    button_4 = types.KeyboardButton('Перезапуск')  # Кнопка для возврата
    markup.row(button_1)
    markup.row(button_2)
    markup.row(button_3)
    markup.row(button_4)  # Добавление кнопки возврата в меню
    bot.send_message(message.chat.id, 'Привет! Выбери следующее действие', reply_markup=markup)
    bot.register_next_step_handler(message, click)

def click(message):
    # Сохранение состояния
    state = user_state.get(message.chat.id, 'main_menu')
    
    if state != 'main_menu':
        return start(message)  # Возвращаем в меню, если состояние не соответствует
    
    if message.text == 'Отобразить графики в чате':
        last_file = os.listdir('D:/DataPy/DataTelegramBot/images')[0]
        file = open('D:/DataPy/DataTelegramBot/images/' + last_file, 'rb')
        bot.send_photo(message.chat.id, file)
        bot.register_next_step_handler(message, click)

    elif message.text == 'Перейти в Google sheets':
        markup_for_button_link = types.InlineKeyboardMarkup()
        markup_for_button_link.add(types.InlineKeyboardButton('GS', url='https://docs.google.com/spreadsheets/d/1h8RrekZGeL4NfZ8_6sJpaW_RSv7NS3KDhaP5k3RWlT8/edit?usp=sharing'))
        bot.send_message(message.chat.id, 'Ссылка:', reply_markup=markup_for_button_link)
        bot.register_next_step_handler(message, click)

    elif message.text == 'Получить данные в формате txt':
        last_file = os.listdir('D:/DataPy/DataTelegramBot/reports')[0]
        file = open('D:/DataPy/DataTelegramBot/reports/' + last_file, 'rb')
        bot.send_document(message.chat.id, file)
        bot.register_next_step_handler(message, click)

    elif message.text == 'Перезапуск':  # Если нажата кнопка возврата
        start(message)  # Вызов функции start для возврата в главное меню

bot.polling(none_stop=True)