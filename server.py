import RPi.GPIO as GPIO
import Adafruit_DHT
import _mysql
import MySQLdb as mdb
import time
from datetime import datetime as dt
import pytz

GPIO_DHT = 22

DHT_HUM_ID = 0
DHT_TEMP_ID = 0

#Creates connection with the database
#Returns connection and cursor  
def conn():
    con = mdb.connect('localhost', 'root', 'root', 'Fluxuskondenzator')
    cur = con.cursor()
    return cur,con


#Returns the type of the sensor by name     
def getSensorTypeByName(name):
    cur,con=conn()
    query = "SELECT sensorTypeID FROM SensorTypes where sensorName='%s'" % (name)
    cur.execute(query)
    type=cur.fetchone()
    return type[0]

def getSensorValuesByID(id):
    cur, con = conn()
    query = "SELECT date,value FROM Datas where sensorTypeID='%s'" % (id)
    cur.execute(query)
    values = cur.fetchall()
    listDatas = []
    for value in values:
        listDatas.append(value)
    return listDatas

def getSensorLastValueByID(id):
    cur,con=conn()
    query = "SELECT date,value FROM Datas where sensorTypeID='%s' order by date desc" % (id)
    cur.execute(query)
    type=cur.fetchone()
    return type[0],type[1]


#Insert received or sent messages in the database
def insertDataBySensorID(id, value):
    cur,con=conn()
    time = dt.now(pytz.utc)
    query = "INSERT INTO Datas (sensorTypeID,value, date) VALUES ('%s', '%s', NOW())" % (id,value)
    cur.execute(query)
    con.commit()
    return

def readDht():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, GPIO_DHT)
    return humidity, temperature

def readSensors():
    hum, temp = readDht()
    insertDataBySensorID(DHT_TEMP_ID, temp)
    insertDataBySensorID(DHT_HUM_ID, hum)


DHT_HUM_ID = getSensorTypeByName("Humidity")
DHT_TEMP_ID = getSensorTypeByName("Temperature")

readSensors()

#list = getSensorValuesByID(DHT_HUM_ID)
#for data in list:
#    print data[0]
#    print data[1]

print getSensorLastValueByID(DHT_HUM_ID)

print getSensorLastValueByID(DHT_TEMP_ID)