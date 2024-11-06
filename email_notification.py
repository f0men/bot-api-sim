import os

import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv

dirname = os.path.dirname(__file__) # сохрнение название директори текущего файла

dotenv_path = os.path.join(dirname, '.env') # сохранение директории env-файла
load_dotenv(dotenv_path) # загрузка данных env-файла

PASSWORD_EM = os.getenv('PASSWORD')

def message_to_emp(to_lst):
    SENDER = 'jame.ost@mail.ru'
    PASSWORD = PASSWORD_EM
    SMTP_SERVER = 'smtp.mail.ru'
    PORT = 465
    context = ssl.create_default_context()
    msg = EmailMessage()
    subject = "Информация о загрузке данных. Сообщение от бота"
    message = "Данные загружены, отчет можно посмотреть в Google Sheets."
    for i in to_lst: # проходимся по списку лиц, которым нужно отправить рассылку
        msg.set_content(message)
        msg['Subject'] = subject
        msg['From'] = SENDER
        msg['To'] = i
        server = smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context)
        server.login(SENDER, PASSWORD)
        server.send_message(msg=msg)


