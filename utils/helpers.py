import json
from datetime import datetime
import datetime
import time
from sqlalchemy import create_engine
import requests
from abc import ABC, abstractmethod


class Mdict:
    def __init__(self, _dict: dict):
        self.dict = _dict

    def __add__(self, my_dict: any)-> dict:
        self.dict.update(my_dict.dict)
        return self.dict


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


def datetime_formatter_method_decorator(datetime_format_string="%Y-%m-%d"):
    def internal_function(function):
        def wrapper(*args, **kwargs):
            try:
                return datetime.strptime(function(*args, **kwargs), datetime_format_string)
            except Exception:
                return datetime.now()
        return wrapper
    return internal_function


def datetime_formatter_api_json_error_decorator(function):
    def internal_function(*args, **kwargs):
        res = function(*args, **kwargs)
        try:
            return datetime.strptime(res, "%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            return datetime.now()

    return internal_function


def aviasales_api_json_error_decorator(function):
    def internal_function(*args, **kwargs):
        res = function(*args, **kwargs)
        if isinstance(res, dict):
            if 'errors' in res.keys() and len(res['errors']) > 0:
                raise Exception('Data error occurred: %s ' % res['errors'])
        else:
            return res
    return internal_function


def getJsonData(url):
    try:
        response = requests.get(url).json()
    except json.decoder.JSONDecodeError:
        print(u"Проверьте правильность вызова {} в браузере, в ответе должен возвращаться json".format(url))
        return
    except Exception as e:
        print(e)
    else:
        return response



def run_sql_file(filename: str, conn_sring: str):
    """
    The function takes a filename and a connection as input
    and will run the SQL query on the given connection
    """
    start = time.time()

    file = open(filename, 'r')
    sql = " ".join(file.readlines())

    engine = create_engine(conn_sring)

    print("Start executing: " + filename + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + "\n" + sql)

    with engine.connect() as con:
        rs = con.execute(sql)

    end = time.time()
    print("Time elapsed to run the query:")
    print(str((end - start) * 1000) + ' ms')

    return rs