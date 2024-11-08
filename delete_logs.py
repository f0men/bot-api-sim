import os

def delete_logs(dir):
    files = sorted(os.listdir(dir)[:-3])
    for file in files:
        os.remove(f'{dir}/{file}')

