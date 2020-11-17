import requests
import json
url = 'http://127.0.0.1:8080'

print('                                                                                             GET')
print('Время на сервере ' + requests.get(url).text)
print('Время в определенной зоне' + requests.get(url+'/America/Toronto').text)
print('Неверная зона ' + requests.get(url+'/Asia/ew').text)

print('                                                                                             POST')

data = {'type': 'time'}
print('Время без параметров: ' + requests.post(url=url, data=json.dumps(data)).text)
data = {'type': 'date'}
print('Дата без параметров: ' + requests.post(url=url, data=json.dumps(data)).text)
data = {'tz_start': 'America/Toronto', 'tz_end': 'Europe/London', 'type': 'datediff'}
print('Разница во времени: ' + requests.post(url=url, data=json.dumps(data)).text)
data = {'tz_start': 'Etc/GMT-8', 'tz_end': 'Etc/GMT+8', 'type': 'datediff'}
print('Разница в дате: ' + requests.post(url=url, data=json.dumps(data)).text)
data = {'tz_end': 'America/Toronto', 'type': 'datediff'}
print('Отсутсвует начальный аргумент: ' + requests.post(url=url, data=json.dumps(data)).text)
data = {'tz_start': 'Europe/London', 'type': 'datediff'}
print('Отсутствует конечный аргумент: ' + requests.post(url=url, data=json.dumps(data)).text)
data = {'type': 'datediff'}
print('Отсутвуют начальный и конечный аргумент: ' + requests.post(url=url, data=json.dumps(data)).text)
data = {'tz_start': 'Europe/London', 'tz_end': 'Canada/Pacific'}
print('Отсутствует тип: ' + requests.post(url=url, data=json.dumps(data)).text)
data = {'tz_start': 'Europe/Lolndon', 'tz_end': 'America/Toronto', 'type': 'datediff'}
print('Ошибка в первом аргументе : ' + requests.post(url=url, data=json.dumps(data)).text)
data = {'tz_start': 'America/Toronto', 'tz_end': 'Europe/Lolndon', 'type': 'datediff'}
print('Ошибка во втором аргументе : ' + requests.post(url=url, data=json.dumps(data)).text)



