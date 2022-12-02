from machine import Timer, RTC, Pin
import time
import ntptime


def syncTime(t):
    try:
        ntptime.settime()
        print(rtc.datetime())
        print("%d seconds left,current temp:%d"%(nextTime,currentTemp))
        return True
    except Exception as e :
        print('sync time error')
        print(e)
        return False
   
        

def switchLogic(t):
    if currentTemp == NIGHT_TEMP:
        setDayTemp()
    else:
        setNightTemp()
    
    # nexTime = time.time()+43200#12 hours
    while not syncTime(0):
        print('60 seconds to retry')
        time.sleep(60)
    setNextTimer()
    
def setNextTimer():
    global currentTemp,nextTime
    t = time.localtime()
    year = t[0]
    month = t[1]
    day = t[2]
    hour = t[3]

    nTime = 0
    if hour >= 8 and hour < 20:
        nTime = (year,month,day,20,0,0,0,0)
    elif hour < 8:
        nTime = (year,month,day,8,0,0,0,0)
    else:
        torrow = time.time() + 14400#4 hours
        tt = time.localtime(torrow)
        nTime = (tt[0],tt[1],tt[2],8,0,0,0,0)

    nextTime = time.mktime(nTime) - time.time()
    tim1.init(period=nextTime*1000, mode=Timer.ONE_SHOT, callback=switchLogic)




def low():
    global currentTemp
    pinLow.off()
    time.sleep_ms(pressDelay)
    pinLow.on()
    if currentTemp>30 :
        currentTemp -= 1
    print(currentTemp)
    time.sleep_ms(pressDelay)


def high():
    global currentTemp
    pinHigh.off()
    time.sleep_ms(pressDelay)
    pinHigh.on()
    if currentTemp < 55:
        currentTemp += 1
    print(currentTemp)
    time.sleep_ms(pressDelay)


def reset():
    i = 0
    while i < 20:
        low()
        i += 1


def setTemp(temp):
    if temp > currentTemp:
        while temp > currentTemp:
            high()
    elif temp < currentTemp:
        while temp < currentTemp:
            low()

def setNightTemp():
    setTemp(NIGHT_TEMP)
    print('setNightTemp')

def setDayTemp():
    setTemp(DAY_TEMP)
    print('setDayTemp')

NIGHT_TEMP = 50
DAY_TEMP = 30
pressDelay = 80
currentTemp = DAY_TEMP

ntptime.NTP_DELTA = 3155644800
ntptime.host = "ntp.aliyun.com"
pinLow = Pin(0, Pin.OUT, value=1)
pinHigh = Pin(2, Pin.OUT, value=1)
rtc = RTC()

tim0 = Timer(0)
tim1 = Timer(1)
nextTime = 0

while not syncTime(0):
    print('10 seconds to retry')
    time.sleep(10)

t = time.localtime()
hour = t[3]

if hour >= 8 and hour < 20:
    currentTemp = DAY_TEMP
else:
    currentTemp = NIGHT_TEMP


setNextTimer()

tim0.init(period=600000, mode=Timer.PERIODIC, callback=syncTime)
