
import copy
from sqlalchemy import create_engine
from mapping import weather_mapper, flytickets_mapper
import json
import credentials
from utils.helpers import Mdict, run_sql_file

from abc import ABC, abstractmethod

class Builder(ABC):
    """
    Интерфейс Строителя объявляет создающие методы для различных частей объектов
    Продуктов.
    """

    @abstractmethod
    def product(self) -> None:
        pass

    @abstractmethod
    def produce_part_a(self) -> None:
        pass

    @abstractmethod
    def produce_part_b(self) -> None:
        pass

    @abstractmethod
    def produce_part_c(self) -> None:
        pass

    @abstractmethod
    def produce_part_d(self) -> None:
        pass

class ConcreteBuilder1(Builder):
    """
    Классы Конкретного Строителя следуют интерфейсу Строителя и предоставляют
    конкретные реализации шагов построения. Ваша программа может иметь несколько
    вариантов Строителей, реализованных по-разному.
    """

    def __init__(self) -> None:
        """
        Новый экземпляр строителя должен содержать пустой объект продукта,
        который используется в дальнейшей сборке.
        """
        self.reset()

    def reset(self) -> None:
        self._product = Product1()

    @property
    def product(self):
        """
        Конкретные Строители должны предоставить свои собственные методы
        получения результатов. Это связано с тем, что различные типы строителей
        могут создавать совершенно разные продукты с разными интерфейсами.
        Поэтому такие методы не могут быть объявлены в базовом интерфейсе
        Строителя (по крайней мере, в статически типизированном языке
        программирования).

        Как правило, после возвращения конечного результата клиенту, экземпляр
        строителя должен быть готов к началу производства следующего продукта.
        Поэтому обычной практикой является вызов метода сброса в конце тела
        метода getProduct. Однако такое поведение не является обязательным, вы
        можете заставить своих строителей ждать явного запроса на сброс из кода
        клиента, прежде чем избавиться от предыдущего результата.
        """
        product = self._product
        self.reset()
        return product

    def produce_part_a(self) -> None:
        self._product.form_db_list_with_routes()

    def produce_part_b(self) -> None:
        self._product.form_list_with_cheap_ticket_flights('MOW')

    def produce_part_c(self) -> None:
        self._product.form_list_with_weather_info()

    def produce_part_d(self) -> None:
        self._product.make_file(directory='../files/Moscow', filename='MOW_weather_tickets.json')


_sql = "Select a.arrival_city_iata,b.name_translations as arrival_city_name from ( Select distinct b.city_code as departure_city_iata ,c.city_code as arrival_city_iata from public.routes as a inner join public.iata_mapping as b on a.departure_airport_iata = b.code inner join public.iata_mapping as c on a.arrival_airport_iata = c.code where b.city_code = '{origin}' ) a inner join public.cities b on a.arrival_city_iata = b.code inner join public.cities c on a.departure_city_iata = c.code".format(origin="MOW")
_conn_string = 'postgres://{user}:{password}@vacation-planner-library.ciodtn8hce9y.ap-south-1.rds.amazonaws.com:5432/postgres'.format(user=credentials.DB_LOGIN, password=credentials.DB_PASSWORD)
_engine = create_engine(_conn_string)


class Product1():
    """
    В методах продукта содержатся все необходимые для получения готового результата методы. 1) Он делает запрос к базе
    данных 2) Запрашивает внешний api для поиска билетов 3)...
    """

    def __init__(self) -> None:
        self._routes = []
        self._flights = []
        self._weather = []

    def form_db_list_with_routes(self) -> None:

        rs = run_sql_file('../sql/get_routes_moscow.sql', credentials.DATABASE_ENDPOINT)
        for row in rs:
            self._routes.append(
                {
                    "arrival_iata": row[0]
                    , "name": row[1]
                }
            )

    def form_list_with_cheap_ticket_flights(self, origin: str) -> None:
        if self._routes:
            for route in self._routes:
                for item in flytickets_mapper.get_cheap_prices(origin, route['arrival_iata']):
                    item.data.update(route)
                    self._flights.append(item.data)

    def form_list_with_weather_info(self) -> None:
        for item in self._flights:
            weather_json = weather_mapper.weather_data(item['name']).form_json()
            aviasales_item = copy.deepcopy(item)
            self._weather.append(Mdict(weather_json) + Mdict(aviasales_item))

    def make_file(self, directory: str, filename: str):
        with open("{path}/{filename}".format(path=directory, filename=filename), "w+") as wf:
            json.dump(self._weather, wf)

class Director:
    """
    Директор отвечает только за выполнение шагов построения в определённой
    последовательности. Это полезно при производстве продуктов в определённом
    порядке или особой конфигурации. Строго говоря, класс Директор необязателен,
    так как клиент может напрямую управлять строителями.
    """

    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        """
        Директор работает с любым экземпляром строителя, который передаётся ему
        клиентским кодом. Таким образом, клиентский код может изменить конечный
        тип вновь собираемого продукта.
        """
        self._builder = builder

    """
    Директор может строить несколько вариаций продукта, используя одинаковые
    шаги построения.
    """

    def build_file_to_upload(self) -> None:
        self.builder.produce_part_a()
        self.builder.produce_part_b()
        self.builder.produce_part_c()
        self.builder.produce_part_d()



if __name__ == "__main__":

    director = Director()
    builder = ConcreteBuilder1()
    director.builder = builder

    director.build_file_to_upload()

