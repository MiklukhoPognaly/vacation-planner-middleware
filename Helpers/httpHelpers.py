import requests
import unittest
import json
import json

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


def getJsonDataRaw(url):
    try:
        response = requests.get(url).text
    except json.decoder.JSONDecodeError:
        print(u"Проверьте правильность вызова {} в браузере, в ответе должен возвращаться json".format(url))
        return
    except Exception as e:
        print(e)
    else:
        return list(response)


