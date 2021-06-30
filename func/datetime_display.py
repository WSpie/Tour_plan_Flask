import datetime
import pytz

def get_today():
    current_time = datetime.datetime.now()
    month = current_time.month
    day = current_time.day
    if len(str(month)) == 1:
        month = '0' + str(month)
    if len(str(day)) == 1:
        day = '0' + str(day)
    return f'{current_time.year}-{month}-{day}'

def datetime_display():
    current_time = datetime.datetime.now()
    china_timezone = pytz.timezone('Asia/Shanghai')
    tamu_timezone = pytz.timezone('US/Central')
    china_time = china_timezone.localize(current_time)
    tamu_time = china_time.astimezone(tamu_timezone)
    return f'Shanghai: {china_time.year}-{china_time.month}-{china_time.day} {china_time.hour}:{china_time.minute}     ' \
           f'TAMU: {tamu_time.year}-{tamu_time.month}-{tamu_time.day} {tamu_time.hour}:{tamu_time.minute}'