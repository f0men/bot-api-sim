import os

def delete_logs(dir):
    files = os.listdir(dir)[:-3]
    files.sort()
    for file in files:
        os.remove(f'{dir}/{file}')

