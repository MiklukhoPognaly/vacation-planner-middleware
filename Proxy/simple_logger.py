from abc import ABC, abstractmethod
import requests

class Subject(ABC):
    """
    Интерфейс Субъекта объявляет общие операции как для Реального Субъекта, так
    и для Заместителя. Пока клиент работает с Реальным Субъектом, используя этот
    интерфейс, вы сможете передать ему заместителя вместо реального субъекта.
    """

    @abstractmethod
    def request(self, url) -> str:
        pass


class GetHttpRequest(Subject):

    def request(self, url) -> str:
        return requests.get(url).text


class ProxyHttpLogger(Subject):

    def __init__(self, http_request_class: GetHttpRequest):
        self._http_request = http_request_class

    def request(self, url) -> str:
        _r = self._http_request.request(url)
        self.log_request(_r)
        return _r

    def log_request(self, mes) -> None:
        print(mes)
