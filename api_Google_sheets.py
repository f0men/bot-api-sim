import gspread
import datetime
import os
import json
from datetime import date
from datetime import timedelta

from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

yesterday_date = datetime.datetime.strftime(date.today()-timedelta(days=1),"%Y-%m-%d")

dirname = os.path.dirname(__file__)

def write_daily_info(data):
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file',
         'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(f'{dirname}/dailyreportspythongs-fe6d3bc3bc0f.json', scope)
    gc = gspread.authorize(credentials)
    sheet = gc.open("daily_activity").worksheet('Sheet1')
    sheet.update_acell("A1", 'Number of attempts')
    sheet.update_acell("B1", 'Number of successful attempts')
    sheet.update_acell("C1", 'Number of unique users')
    sheet.update_acell("A2", data[0])
    sheet.update_acell("B2", data[1])
    sheet.update_acell("C2", data[2])
    sheet.update_acell("E1", 'Report date')
    sheet.update_acell("E2", yesterday_date)