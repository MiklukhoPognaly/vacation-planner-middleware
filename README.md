# Техническое описание проекта

### Описание 

Проект используется в качестве middleware решения для обработки и обеспечения различной логики 
вызовов внешних API.

### Установка

`{{WIP}}`


### Структура каталогов
* files
* logic
* mapping
* services
* sql
* tests (to be updated)
* utils (deprecated)
* venv(deprecated)
* корень проекта

## files

Каталог для хранения файлов для загрузки и индексации в elasticsearch.

## logic

Каталог для хранения программных файлов, обеспечивающих хранение и обработки бизнес-логики приложения.

На текущий момент в каталоге содержится один файл `tickets.py`. В модуле применяется паттерн `builder`.


#### class Builder

Интерфейс Строителя объявляет создающие методы для различных частей объектов
Продуктов.

#### class ConcreteBuilder1(Builder):

Классы Конкретного Строителя следуют интерфейсу Строителя и предоставляют конкретные реализации шагов построения. Ваша программа может иметь несколько 
вариантов Строителей, реализованных по-разному.

В класс инъекцией помещается инстанс класса `Product`

В данном случае реализация вызывает последовательно функции `form_db_list_with_routes()` ->
`form_list_with_cheap_ticket_flights('MOW')` -> `form_list_with_weather_info()` -> `make_file(
            directory=config.UPLOAD_FILE, filename='MOW_weather_tickets.json')`


#### class Product1:
В методах продукта содержатся все необходимые для получения готового результата методы.  
В классе описана логика следующих методов

1. Получения списка маршрутов из базы данных `form_db_list_with_routes(self)`.
2. Формирования списка самых дешевых билетов `form_list_with_cheap_ticket_flights`.
3. Формирования списка с информацией о погоде `form_list_with_weather_info(self)`.
4. Формирования файла для последующей загрузки в ELK `make_file(self, directory: str, filename: str)`.


#### class Director:
Директор отвечает только за выполнение шагов построения в определённой последовательности. Это полезно при производстве продуктов в определённом
порядке или особой конфигурации. 

Строго говоря, класс Директор необязателен, так как клиент может напрямую управлять строителями.


В данной реализации вызывается весь сборочный путь продукта.

```python
def build_file_to_upload(self) -> None: 
    self.builder.produce_part_a()
    self.builder.produce_part_b()
    self.builder.produce_part_c()
    self.builder.produce_part_d()
```

#### Пример вызова 

Сборку файла можно вызвать следующими инструкциями.

```python
director = Director()
builder = ConcreteBuilder1()
director.builder = builder
director.build_file_to_upload()
```


## mapping

Каталог для хранения объектов выполняющих преобразование и конвертацию типов и данных из различных источнников.
На текущий момент в каталоге находятся следующие модули:
1. mapticket.py
2. mapweather.py

#### maptickets.py

Функция `get_cheap_prices` запрашивает информацию из api `http://api.travelpayouts.com/v1/prices/cheap`

```
def get_cheap_prices(iata_town_origin, iata_town_destination) -> BasePricesCheap(response, iata_town_destination).object_list:
```
Класс `BasePricesLatest` выполняет обработку json получаемого посредством вызова внешнего API.

Класс `BasePricesCheap` выполняет обработку json получаемого посредством вызова внешнего API.

Класс `BasePricesMonthMatix` выполняет обработку json получаемого посредством вызова внешнего API.

Класс `BasePricesDirect` выполняет обработку json получаемого посредством вызова внешнего API.

Класс `BasePricesCalendar` выполняет обработку json получаемого посредством вызова внешнего API.

Класс `BasePricesNearestPlacesMatrix` выполняет обработку json получаемого посредством вызова внешнего API.


#### mapweather.py

Класс `WeatherApiDataFacade` выполняет обработку json получаемого посредством вызова внешнего API.

Функция `weather_data` формирует json объект на основе класса обертки `WeatherApiDataFacade`

```
def weather_data(en_city_name, url='http://api.weatherstack.com/current') -> WeatherApiDataFacade(response_json)
```

## Services

Каталог для хранения логики взаимодействия с внешними сервисами.
Содержит модуль:
1. elasticsearch.eservice

#### eservice.py

Выполняется создание глобальной переменной `elastic`, в неё помещается вызов инстанса Elasticsearch driver.
```python
elastic = Elasticsearch(el)
```

Фукнция `script_path` возвращающая текущий каталог в файловой системе.
```python
def script_path():
    path = os.path.dirname(os.path.realpath(__file__))
    if os.name == 'posix': # posix is for macOS or Linux
        path = path + "/"
    else:
        path = path + chr(92) # backslash is for Windows
    return path
```

Функция `get_data_from_file` получает данные из файла, возвращая json объект.
```python
def get_data_from_file(path):
    with open(path, encoding="utf8", errors='ignore') as wf:
        data = wf.read()
    return json.loads(data)
```


Функция `setup_mapping` определяет мэппинг данных в определенном индексе Elasticsearch.
```python
def setup_mapping(index, body, doc_type,):
    elastic.indices.put_mapping(
        index=index,
        doc_type=doc_type,
        body=body,
        include_type_name=True
    )
```

Функция `bulk_json_data` выполняющая загрузку массива документов в индекс Elasticsearch
```python
def bulk_json_data(json_file, _index, doc_type):
    json_list = get_data_from_file(json_file)
    for doc in json_list:
        if '{"index"' not in doc:
            yield {
                "_index": _index,
                "_type": doc_type,
                "_id": uuid.uuid4(),
                "_source": doc
            }
```

Функция `delete_all` удаляющая все индексы и данные из Elasticsearch.

**Осторожно!** При вызове функции `delete_all` произойдет удалени системных индексов, например `.kibana`.
Лучше использовать функцию `delete_index`

```python
def delete_all(url):
    _r = requests.delete(url)
    return _r.text
```

Функция `display_current_mapping` возвращает мэппинг индекса.
```python

def display_current_mapping(base_url, old_index, changed_mapping):
    r = requests.get('{base_url}/{index_name}'.format(base_url=base_url, index_name=old_index))
    r.raise_for_status()
    content = r.json()
    mappings = content[old_index]['mappings']
    mappings['properties'].update(changed_mapping)
    return mappings

```

Фукнция `create_index` cоздаёт индекс в Elasticsearch

```python

def create_index(base_url, new_index, mappings):
    r = requests.put('{base_url}/{index_name}'.format(base_url=base_url, index_name=new_index), json={
        'mappings': mappings
    })
    r.raise_for_status()
    return
```

Функция `perform_reindex` переименовывает индекс
```python
def perform_reindex(base_url, old_index, new_index):
    r = requests.post('{base_url}/_reindex'.format(base_url=base_url), json={
        "source": {
            "index": old_index
        },
        "dest": {
            "index": new_index
        }
    })
    r.raise_for_status()
    return

```

Функция `delete_index` удаляет индекс вместе с данными
```python
def delete_index(base_url, old_index):
    """
    function delete old index
    :param base_url:
    :param old_index:
    :return: None
    """
    r = requests.delete('{base_url}/{index_name}'.format(base_url=base_url, index_name=old_index))
    r.raise_for_status()
    return

```

Функция `create_alias` создает alias для старого индекса 
```python

def create_alias(base_url, new_index, old_index):
    """
    Create an alias (so that on next time this will be easier to do without downtime)
    :param base_url:
    :param new_index:
    :param old_index:
    :return:
    """
    r = requests.post('{base_url}/_aliases'.format(base_url=base_url), json={
        "actions": [
            {"add": {
                "alias": old_index,
                "index": new_index
            }}
        ]
    })
    r.raise_for_status()
    return
```

Класс `PerformUpload` является клиентским классом для загрузки файлов в индекс Elasticsearch.

## sql

Каталог для хранения `.sql` файлов для БД.

На текущий момент находится один скрипт `get_routes_moscow` выполняющий поиск маршрутов из БД.
```dbn-psql
Select distinct
  c.city_code as arrival_iata
  ,d.name_translations as name
  ,e.rus_name as counry_name
  ,e.world_part
  ,e.location
  ,d.sea_vacation
  ,d.ski_vacation
from public.routes as a
inner join
public.iata_mapping as b
on a.departure_airport_iata = b.code
inner join public.iata_mapping as c
on a.arrival_airport_iata = c.code
inner join public.cities d
on d.code = c.city_code
inner join public.countries e
on d.country_code = e.iata_2
where b.city_code = 'MOW';
```

## корень проекта 

#### client.py

Главный клиентский файл, вызывающий все остальные. Лежит в корне проекта.

```python
def client_job():
    director = tickets.Director()
    builder = tickets.ConcreteBuilder1()
    director.builder = builder
    director.build_file_to_upload()
    Upload = eservice.PerformUpload(
            elastic_url=config.elastic_url,
            mapping=config.elastic_data_mapping)
    Upload.perform_upload(filename_path=os.path.join(config.UPLOAD_FILE, 'MOW_weather_tickets.json')
                              , doc_type=config.doc_type
                              , index_name=config.elastic_index_name)

client_job()
```

#### credentials.py
Файл в котором лежат ключи для доступа к внешним API и БД.

Не лежит в общем репозитории.

#### config.py

Файл для хранения различных настроек проекта.

Содержит переменную в которую передается инстанс главного логгера 
```python
logging.config.fileConfig('logging.conf')
main_logger = logging.getLogger('mainExample')
```
Настройки логгера находятся в файле `logger.conf`

Cодержит данные `elastic_index_name`, `elastic_data_mapping`, `doc_type`, `elastic_url` 
для загрузки в elasticsearch

Содержит данные для подключения и взаимодействия с БД.

```python
SQL_FILE = './sql/get_routes_moscow.sql'
UPLOAD_FILE = './files/Moscow'
```