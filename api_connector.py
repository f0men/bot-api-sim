import logging
import requests

class APIConnector:
    
    def __init__(self, api_url):
        self.api_url = api_url
        self.__params = {}
    
    def append_change_params(self, **kwargs):
        for ind, value in kwargs.items():
            self.__params[ind] = value

    def get_params(self):
        return self.__params

    def request_get(self): # отправка get-запроса
        try:
            logging.info('Начало загрузки данных по API')
            get_req = requests.get(self.api_url, self.__params)
            logging.info('Конец загрузки данных по API')
            get_req.raise_for_status()
            res = get_req.json()
            return res
        except requests.exceptions.HTTPError as err:
            logging.error(err)