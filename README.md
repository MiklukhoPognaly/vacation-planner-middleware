# Техническое описание проекта

### Структура каталогов
* files
* logic
* mapping
* services
* sql
* tests
* utils
* venv(deprecated)

### files

Каталог для хранения файлов для загрузки и индексации в elasticsearch.

### logic

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

```
def build_file_to_upload(self) -> None: 
    self.builder.produce_part_a()
    self.builder.produce_part_b()
    self.builder.produce_part_c()
    self.builder.produce_part_d()
```

#### Пример вызова 

Сборку файла можно вызвать следующими инструкциями.

```
director = Director()
builder = ConcreteBuilder1()
director.builder = builder
director.build_file_to_upload()
```
