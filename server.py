import RPi.GPIO as GPIO
import Adafruit_DHT
import _mysql
import MySQLdb as mdb
import time
import serial
from datetime import datetime as dt
import json
import requests
from dweet import Dweet

GPIO_DHT = 22

DHT_HUM_ID = 0
DHT_TEMP_ID = 0

PROJECT_NAME = "Fluxuskondenzator"
DWEET_ID = PROJECT_NAME + "_2017"

DB_NAME = PROJECT_NAME
DB_HOST = 'localhost'
DB_USERNAME = 'root'
DB_PASSWORD = 'root'

STR_HUMIDITY = 'Humidity'
STR_TEMPERATURE = 'Temperature'
STR_DISTANCE = 'Distance'

ser = serial.Serial('/dev/ttyUSB0', 9600)

dweet = Dweet()

#Creates connection with the database
#Returns connection and cursor  
def conn():
    con = mdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME)
    cur = con.cursor()
    return cur,con


#Returns the type of the sensor by name     
def getSensorTypeByName(name):
    cur,con=conn()
    query = "SELECT sensorTypeID FROM SensorTypes where sensorName='%s'" % (name)
    cur.execute(query)
    type=cur.fetchone()
    return type[0]

#Returns all the values for the Sensor with id
def getSensorValuesByID(id):
    cur, con = conn()
    query = "SELECT date,value FROM Datas where sensorTypeID='%s'" % (id)
    cur.execute(query)
    values = cur.fetchall()
    listDatas = []
    for value in values:
        listDatas.append(value)
    return listDatas

#Returns the last value for the sensor with id
def getSensorLastValueByID(id):
    cur,con=conn()
    query = "SELECT date,value FROM Datas where sensorTypeID='%s' order by date desc" % (id)
    cur.execute(query)
    type=cur.fetchone()
    return type[0],type[1]


#Insert received or sent messages in the database
def insertDataBySensorID(id, value):
    cur,con=conn()
    query = "INSERT INTO Datas (sensorTypeID,value, date) VALUES ('%s', '%s', NOW())" % (id,value)
    cur.execute(query)
    con.commit()
    return

def insertDataBySensorName(name, value):
    print name + " " + value
    id = getSensorTypeByName(name)
    insertDataBySensorID(id,value)
    return

#Reads the data from the DHT sensor
def readDht():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, GPIO_DHT)
    return humidity, temperature

#Reads all the sensors
def readSensors():
	resp = ser.readline()
	resp_splitted = resp.split(',')
	
	hum = 0
	temp = 0
	dist = 0
	
	list = []
	for word in resp_splitted:
		if word.find(':') != -1:
			type, data = word.split(':', 1)
			insertDataBySensorName(type, data)
			if type == STR_HUMIDITY:
				hum = data
			elif type == STR_TEMPERATURE:
				temp = data
			elif type == STR_DISTANCE:
				dist = data
				
	return hum, temp, dist

#Inserts the data into the database
def insertDataIntoDatabase(hum, temp):
    insertDataBySensorID(DHT_HUM_ID, hum)
    insertDataBySensorID(DHT_TEMP_ID, temp)

#Sends the sensor data to dweet.io and returns 'success' on success and 'failed' on failure
def sendData(hum, temp, dist):
	try:
		resp = dweet.dweet_by_name(name=DWEET_ID, data={STR_HUMIDITY : hum, STR_TEMPERATURE : temp, STR_DISTANCE : dist})
		resp_json = json.loads(json.dumps(resp))
		return resp['this']
	except requests.exceptions.ConnectionError:
		return "Connection error"

#Test method wichi will print the data, send it to dweet.io and print the result
def uploadToDweet(hum, temp, dist):
	print "Sending"
	print "\tHumidity: ", hum
	print "\tTemperature: ", temp
	print "\tDistance: ", dist
	
	resp = sendData(hum, temp, dist)
	print "Result: " + resp + '\n'	

#Loop which will read the sensors, save the data in databas and send it to dweet.io
def mainLoop():

	while True:
		hum, temp, dist = readSensors()
		# insertDataIntoDatabase(hum, temp)
		# sendData(hum, temp)
		uploadToDweet(hum, temp, dist)
		time.sleep(1)


if __name__ == "__main__":
#	DHT_HUM_ID = getSensorTypeByName(STR_HUMIDITY)
#	DHT_TEMP_ID = getSensorTypeByName(STR_TEMPERATURE)
#	DIST_ID = getSensorTypeByName(STR_DISTANCE)

	#list = getSensorValuesByID(DHT_HUM_ID)
	#for data in list:
	#    print data[0]
	#    print data[1]
	# print getSensorLastValueByID(DHT_HUM_ID)
	# print getSensorLastValueByID(DHT_TEMP_ID)

	mainLoop()
