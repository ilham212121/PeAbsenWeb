from application import app
from time import time
import time
import datetime
a=time.localtime()
hr=a.tm_hour
mn=a.tm_min
sc=a.tm_sec
thn=a.tm_year
mon=a.tm_mon
hari=a.tm_mday
print('{}:{}:{}'.format(hr,mn,sc))
from datetime import datetime
localtime = time.asctime(time.localtime(time.time()))

print ("Waktu lokal saat ini :"+str(hari)+str(mon)+str(thn)+"") #python 2
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
    app.run(debug=True,port=5001)
