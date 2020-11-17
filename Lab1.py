import json
from pytz import timezone
from pytz import UnknownTimeZoneError
from paste.httpserver import serve
from datetime import datetime
from tzlocal import get_localzone


def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type','text/plain; charset=utf-8')]
    format_time = '%H:%M:%S'
    format_date = '%d %b %Y'
    if environ['REQUEST_METHOD'] == 'GET':
        get_timezone = environ['PATH_INFO'][1:]
        if get_timezone:
            try:
                get_timezone = timezone(get_timezone)
                input_text = 'Время в %s:' % get_timezone
            except UnknownTimeZoneError:
                start_response(status,headers)
                return [b'Unknown time zone']
        else:
            get_timezone = None
            input_text = 'Время: '
        start_response(status, headers)
        return [bytes(input_text + datetime.now(tz=get_timezone).strftime(format_time),encoding='utf-8')]

    if 'POST' == environ['REQUEST_METHOD']:
        data = json.loads(environ['wsgi.input'].read().decode("utf-8"))
        try:
            type = data['type']
        except:
            start_response(status,headers)
            return [b'Error in type Data']

        if type == 'date' or type == 'time':
            try:
                zone = data['tz_start']
                try:
                    zone = timezone(zone)
                except UnknownTimeZoneError:
                    start_response(status,headers)
                    return [b'Unknown Time Zone']
                start_response(status,headers)
            except:
                zone = get_localzone()
            date = datetime.now(tz=zone).strftime(format_date)
            time = datetime.now(tz=zone).strftime(format_time)
            start_response(status,headers)
            if type == 'date':
                return [bytes(json.dumps({'Date': date,'TimeZone': str(get_localzone())}),encoding='utf-8')]
            if type == 'time':
                return [bytes(json.dumps({'Time': time,'TimeZone': str(get_localzone())}),encoding='utf-8')]

        if type == 'datediff':
            try:
                zone_start = data['tz_start']
                try:
                    zone_end = data['tz_end']
                except:
                    start_response(status,headers)
                    return [b'Missed 2 or all arguments']
            except:
                start_response(status,headers)
                return [b'Missed 1 or all arguments']
            try:
                zone0 = timezone(zone_start).localize(datetime.now())
                try:
                    zone1 = timezone(zone_end).localize(datetime.now())
                except UnknownTimeZoneError:
                    start_response(status,headers)
                    return [b'2 argument Unknown Time Zone']
            except UnknownTimeZoneError:
                start_response(status,headers)
                return [b'1 argument Unknown Time Zone']
            if datetime.astimezone(zone0) >= datetime.astimezone(zone1):
                diff = str(datetime.astimezone(zone0) - datetime.astimezone(zone1))
            else:
                diff = '-' + str(datetime.astimezone(zone1) - datetime.astimezone(zone0))
            start_response(status,headers)
            return [bytes(json.dumps(
                {'Diff': diff,'Start_zone': str(data['tz_start']),'End_zone': str(data['tz_end'])}),
                encoding='utf-8')]
        start_response(status,headers)
        return [b'Type isn`t identified']


serve(app)
