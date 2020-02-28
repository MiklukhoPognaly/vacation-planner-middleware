from baseClasses import BaseJsonPurifier
import copy
from sqlalchemy import create_engine
from AviasalesFacadeApi import aviasales_partner_api
from WeatherFacadeApi import weatherApi
import json
import credentials

def addToDict(dict1=None, dict2=None):
    chunk = {}
    if not dict1:
        dict1 = {}
    if not dict2:
        dict2 = {}
    chunk.update(dict1)
    chunk.update(dict2)
    return chunk

class FormTicketsInfo(BaseJsonPurifier):
    """
    Class for generating information on tickets from the database and weather methods
    """
    def __init__(self, origin_iata, getRoutes=True, getFlyInfo=True, getWeatherData=True):
        if getRoutes:
            routes = self._get_db_routes(origin_iata)
        if getFlyInfo:
            fly_info = self._get_data_from_aviasales(origin=origin_iata, routes=routes)
        if getWeatherData:
            self.data = self._get_weather_info(fly_info)

    def _get_db_routes(self, origin_iata):
        alist = []
        _raw_sql = "Select " \
                   "a.arrival_city_iata" \
                   ",b.name_translations as arrival_city_name " \
                   "from ( " \
                   "Select distinct " \
                   "b.city_code as departure_city_iata " \
                   ",c.city_code as arrival_city_iata " \
                   "from public.routes as a " \
                   "inner join public.iata_mapping as b " \
                   "on a.departure_airport_iata = b.code " \
                   "inner join public.iata_mapping as c " \
                   "on a.arrival_airport_iata = c.code " \
                   "where b.city_code = '{origin}' " \
                   ") a inner join public.cities b " \
                   "on a.arrival_city_iata = b.code " \
                   "inner join public.cities c " \
                   "on a.departure_city_iata = c.code".format(origin=origin_iata)


        engine = create_engine(
        'postgres://{user}:{password}@vacation-planner-library.ciodtn8hce9y.ap-south-1.rds.amazonaws.com:5432/postgres'
            .format(user=credentials.DB_LOGIN, password=credentials.DB_PASSWORD))

        with engine.connect() as con:
            rs = con.execute(_raw_sql)
            for row in rs:
                alist.append({"arrival_iata": row[0], "name": row[1]})
        print('данные из базы получены')
        return alist

    def _get_data_from_aviasales(self, origin, routes):
        print('Начало получения данных из внешнего источника aviasales')
        alist = []
        if routes:
            for route in routes:
                for item in aviasales_partner_api.get_cheap_prices(origin, route['arrival_iata']):
                    item.data.update(route)
                    alist.append(item.data)
        print('Данные от aviasales получены')
        return alist

    def _get_weather_info(self, fly_info):
        alist = []
        print('Начало получения данных по погоде и локации')
        for item in fly_info:
            weather_json = weatherApi.weather_data(item['name']).form_json()
            aviasales_item = copy.deepcopy(item)
            alist.append(addToDict(weather_json, aviasales_item))
        print('Финальные данные получены')
        return alist

    def get_raw_data(self):
        return self.data

    def form_json(self, path, filename, data=None):
        if data is None:
            data = self.data
        with open("{path}/{filename}".format(path=path, filename=filename), "w+") as wf:
            print('Начало записи в файл {path}/{filename}'.format(path=path, filename=filename))
            json.dump(data, wf)

    def form_json_to_elasticsearch(self, path, filename, data=None):
        if data and isinstance(data, list):
            if not len(data):
                raise ValueError('{data} should have values'.format(data=data))
            if not isinstance(data[0], dict):
                raise ValueError('{data} should contain dictionary'.format(data=data))
            _alist = data
        else:
            _alist = self.get_raw_data()

        with open("{path}/{filename}".format(path=path, filename=filename), "w+") as wf:
            for index in range(0, len(_alist)):
                _meta = '{{"index" : {{ "_index" : "aviasales", "_id" : "{id}" }}'.format(id=index+1)
                _doc = json.dumps(_alist[index])
                _str = _meta+'\n'+_doc+'\n'
                wf.write(_str)

if __name__ == "__main__":
    inst = FormTicketsInfo("MOW")
    inst.form_json_to_elasticsearch('.', '_bulk_fly_info_with_weather.json')
