# импорт необходимых библиотек и модулей
from datetime import date
from datetime import timedelta
from data_add_to_database import data_add_to_database

import logging
import datetime
import json
import os

import configparser
from dotenv import load_dotenv

# импорт классов (модулей) из соседних файлов
from api_connector import APIConnector 
from database_connector import DataBase
from delete_logs import delete_logs
from api_Google_sheets import write_daily_info
from email_notification import message_to_emp
from prep import Preparer

dirname = os.path.dirname(__file__) # сохрнение название директори текущего файла

config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'))

dotenv_path = os.path.join(dirname, '.env') # сохранение директории env-файла
load_dotenv(dotenv_path) # загрузка данных env-файла

DATABASE_CREDS = config['Database'] # подтягиваем данные с конфиг-файла
EMAIL_ADDRESS=config['Users']

API_URL = os.getenv('API_URL') # вытаскиваем url из env-файла
CLIENT = os.getenv('CLIENT') # вытаскиваем логин
CLIENT_KEY = os.getenv('CLIENT_KEY') # вытаскиваем пароль клиента

# настройка логгинга
logging.basicConfig(
    filename=f'{dirname}/logs/{datetime.datetime.strftime(date.today()-timedelta(days=1),"%Y-%m-%d")}.log',
    filemode='a',  # append логов
    format='%(asctime)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)

api_connect = APIConnector(API_URL) # создание экземпляра класса api-соединения

api_connect.append_change_params(client = CLIENT,
                               client_key = CLIENT_KEY,
                               start = datetime.datetime.strftime(datetime.datetime.now()-timedelta(days=1), '%Y-%m-%d %H:%M:%S.%f'),
                               end=datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S.%f')) # добавление параметров подключения

data = api_connect.request_get() # сохранение результата get-запроса


db = DataBase(
    host=DATABASE_CREDS["HOST"],
    database=DATABASE_CREDS["DATABASE"],
    user=DATABASE_CREDS["USER"],
    password=DATABASE_CREDS["PASSWORD"],
    port=DATABASE_CREDS["PORT"]) # создание экземпляра соединения с базой данных

data_add_to_database(data, db) # Добавление данных в базу

delete_logs(f'./logs') # удаление log-файлов, которым больше 3-х дней

lst_for_google_sheets_and_bots = [len(data), len(list(filter(lambda x: x['is_correct']==True, data))), len({i.get('lti_user_id') for i in data})] # формирование ежедневных метрик для отчета
write_daily_info(lst_for_google_sheets_and_bots) # изменение информации в Google Sheets
message_to_emp([str(EMAIL_ADDRESS['USERS'])])

Preparer.delete_photo_reports('./DataTelegramBot/images') #удаление устаревшего изображения графика
Preparer.delete_photo_reports('./DataTelegramBot/reports') # удаление устаревшего текстового файла
Preparer.create_file_daily_activity(lst_for_google_sheets_and_bots,'./DataTelegramBot/reports') # создание файла для отправки ботом
Preparer.make_plot(lst_for_google_sheets_and_bots, './DataTelegramBot/images') # создание изображения с графиком для отправки ботом
