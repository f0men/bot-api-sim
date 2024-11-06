import os

def delete_logs(dir):
    for file in os.listdir(dir)[:-3]:
        os.remove(f'{dir}/{file}')

