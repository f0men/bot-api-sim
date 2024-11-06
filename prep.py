import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from datetime import timedelta


class Preparer:
    
    @staticmethod
    def delete_photo_reports(dir):
        for file in os.listdir(dir):
            os.remove(f'{dir}/{file}')
    
    @staticmethod
    def create_file_daily_activity(lst, dir):
        cur_date = datetime.datetime.strftime(date.today()-timedelta(days=1),"%Y-%m-%d")
        file_dir = f'{dir}' + f'/{cur_date}'
        with open (file_dir,'a') as writer_reports:
            writer_reports.write('Number of attempts' +f' {lst[0]}\n')
            writer_reports.write('Number of successful attempts' +f' {lst[1]}\n')
            writer_reports.write('Number of unique users' +f' {lst[2]}\n')
    
    @staticmethod
    def make_plot(lst, dir):
        
        # Получаем текущую дату
        cur_date = datetime.datetime.strftime(date.today() - timedelta(days=1), "%Y-%m-%d")
        
        # Создаем DataFrame
        df = pd.DataFrame()
        df['count'] = lst
        df.index = ['Number of attempts', 'Number of successful attempts', 'Number of unique users']
        
        # Создаем график
        plt.figure(figsize=(8, 6))  # Размер графика
        bars = plt.bar(df.index, df['count'], color=['#FFDEAD', '#DEB887', '#D2B48C'])  # Цвета столбцов

        # Добавляем заголовок и подписи
        plt.title(f'Daily Activity Report for {cur_date}', fontsize=16)
        plt.xlabel('Activity Type', fontsize=14)
        plt.ylabel('Count', fontsize=14)
        
        # Добавляем значения в центр блоков
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval/2, int(yval), ha='center', va='center', fontsize=12, color='black')

        plt.savefig(os.path.join(dir, f'{cur_date}_plot.png'), format='png', bbox_inches='tight')

        



