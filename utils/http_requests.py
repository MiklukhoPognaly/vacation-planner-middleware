from abc import ABC, abstractmethod
import requests

class HttpGetAbstractClass(ABC):
    """
    Интерфейс Субъекта объявляет общие операции как для Реального Субъекта, так
    и для Заместителя. Пока клиент работает с Реальным Субъектом, используя этот
    интерфейс, вы сможете передать ему заместителя вместо реального субъекта.
    """

    @abstractmethod
    def get_json(self, url) -> dict:
        pass

    @abstractmethod
    def get_text(self, url) -> str:
        pass


class GetJson(HttpGetAbstractClass):
    """
    Простой класс для получения данных из RESTFULL API. Пока реализован только GET
    """
    def get_json(self, url) -> dict:
        return requests.get(url).json()

    def get_text(self, url) -> str:
        return requests.get(url).text


class ProxyLogger(HttpGetAbstractClass):

    """
    Все взаимодействие с классом GetJson проходит через прокси, в случае необходимости можно добавить в
    этот класс обработку ошибок, кэширование, логгирование. Сейчас используется просто вывода в STDIN информации
    по запросу
    """

    def __init__(self, http_request_class: GetJson):
        self._http_request = http_request_class

    def get_json(self, url) -> dict:
        _json = self._http_request.get_json(url)
        self.log_request("Получен json, %s" % _json)
        return _json

    def get_text(self, url) -> str:
        _text = self._http_request.get_text(url)
        self.log_request("Получена строка, %s" % _text)
        return _text

    def log_request(self, mes) -> None:
        print(mes)


def get_json(url) -> dict:
    return ProxyLogger(GetJson()).get_json(url)


#
#
#
# @utils.decorators.aviasales_api_json_error_decorator
# def get_json_raw(url, *querystring):
#     _r = requests.get(url, *querystring)
#     return _r.json()
#
#
# def get_json(url):
#     _ = GetJson()
#     return ProxyLogger(GetJson())
