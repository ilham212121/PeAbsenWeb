from application import app
from time import time
import time
import datetime
a=time.localtime()
hr=a.tm_hour
mn=a.tm_min
sc=a.tm_sec
print('{}:{}:{}'.format(hr,mn,sc))
from datetime import datetime

def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime


timeStart = '06:30AM'
timeEnd = '07:10AM'
if hr>=12:
    hr= hr-12
    w='PM'
else:
    w='AM'
timeNow = '{}:{}{}'.format(hr,mn,w)
timeEnd = datetime.strptime(timeEnd, "%I:%M%p")
timeStart = datetime.strptime(timeStart, "%I:%M%p")
timeNow = datetime.strptime(timeNow, "%I:%M%p")

print(isNowInTimePeriod(timeStart, timeEnd, timeNow))
if __name__ == '__main__':
    app.run(host="10.0.50.0",debug=True,port=5001)
