try:
    import RPi.GPIO as GPIO
    import Adafruit_DHT
    import serial
except ImportError:
    pass
import MySQLdb as mdb
import time
import requests
from dweet import Dweet

class Fkondenz(object):
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

	def __init__(self, _isTest):
		self.testData = None
		self.testData1 = None
		self.testData2 = None
		
		self.isTest = _isTest
		self.dweet = Dweet()
		try:
			self.ser = serial.Serial('/dev/ttyUSB0', 9600)
		except NameError:
			pass
	
	def Fkondenz(self, _isTest):
		self.isTest = _isTest
		self.dweet = Dweet()
		try:
			self.ser = serial.Serial('/dev/ttyUSB0', 9600)
		except NameError:
			pass

	def conn(self):
		"""
		Creates connection with the database
		Returns connection and cursor
		:return:
		"""
		con = mdb.connect(self.DB_HOST, self.DB_USERNAME, self.DB_PASSWORD, self.DB_NAME)
		cur = con.cursor()
		return cur, con


	def getSensorTypeByName(self, name):
		"""
		Returns the type of the sensor by name
		:param name:
		:return:
		"""
		if self.isTest == False:
			cur, con = self.conn()
			query = "SELECT sensorTypeID FROM SensorTypes where sensorName='%s'" % (name)
			cur.execute(query)
			type = cur.fetchone()
			return type[0]
		else:
			return self.testData

		
	def getSensorValuesByID(self, id):
		"""
		Returns all the values for the Sensor with id
		:param id:
		:return:
		"""
		if self.isTest == False:
			cur, con = self.conn()
			query = "SELECT date,value FROM Datas where sensorTypeID='%s'" % (id)
			cur.execute(query)
			values = cur.fetchall()
			listDatas = []
			for value in values:
				listDatas.append(value)
			return listDatas
		else:
			return self.testData


	def getSensorLastValueByID(self, id):
		"""
		Returns the last value for the sensor with id
		:param id:
		:return:
		"""
		if self.isTest == False:
			cur, con = self.conn()
			query = "SELECT date,value FROM Datas where sensorTypeID='%s' order by date desc" % (id)
			cur.execute(query)
			type = cur.fetchone()
			return type[0], type[1]
		else:
			return self.testData, self.testData1


	def insertDataBySensorID(self, id, value):
		"""
		Insert received or sent messages in the database
		:param id:
		:param value:
		:return:
		"""
		if self.isTest == False:
			cur, con = self.conn()
			query = "INSERT INTO Datas (sensorTypeID,value, date) VALUES ('%s', '%s', NOW())" % (id, value)
			cur.execute(query)
			con.commit()
		else:
			self.testData = id
			self.testData1 = value
			
		return


	def insertDataBySensorName(self, name, value):
		if self.isTest == False:
			print name , " " , value
			id = self.getSensorTypeByName(name)
			self.insertDataBySensorID(id, value)
		else:
			self.testData = name
			self.testData1 = value

		return


	def readDht(self):
		"""
		Reads the data from the DHT sensor
		:return:
		"""
		if self.isTest == False:
			humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, self.GPIO_DHT)
			return humidity, temperature
		else:
			return self.testData, self.testData1


	def readSensors(self):
		"""
		Reads all the sensors
		:return:
		"""
		if self.isTest == False:
			resp = ""
			try:
				resp = self.ser.readline()
			except NameError:
				pass
			resp_splitted = resp.split(',')

			hum = 0
			temp = 0
			dist = 0

			for word in resp_splitted:
				if word.find(':') != -1:
					type, data = word.split(':', 1)
					self.insertDataBySensorName(type, data)
					if type == self.STR_HUMIDITY:
						hum = data
					elif type == self.STR_TEMPERATURE:
						temp = data
					elif type == self.STR_DISTANCE:
						dist = data

			return hum, temp, dist
		else:
			return self.testData, self.testData1, self.testData2


	def insertDataIntoDatabase(self, hum, temp):
		"""
		Inserts the data into the database
		:param hum:
		:param temp:
		:return:
		"""
		self.insertDataBySensorID(self.DHT_HUM_ID, hum)
		self.insertDataBySensorID(self.DHT_TEMP_ID, temp)


	def sendData(self, hum, temp, dist):
		"""
		Sends the sensor data to dweet.io and returns 'success' on success and 'failed' on failure
		:param hum:
		:param temp:
		:param dist:
		:return:
		"""
		try:
			resp = self.dweet.dweet_by_name(name=self.DWEET_ID, data={self.STR_HUMIDITY: hum, self.STR_TEMPERATURE: temp, self.STR_DISTANCE: dist})
			return resp['this']
		except requests.exceptions.ConnectionError:
			return "Connection error"


	def uploadToDweet(self, hum, temp, dist):
		"""
		Test method wichi will print the data, send it to dweet.io and print the result
		:param hum:
		:param temp:
		:param dist:
		:return:
		"""
		if self.isTest == False:
			print "Sending"
			print "\tHumidity: ", hum
			print "\tTemperature: ", temp
			print "\tDistance: ", dist

			resp = self.sendData(hum, temp, dist)
			print "Result: " + resp + '\n'
		else:
			self.testData = "Uploaded"


	def mainLoop(self):
		"""
		Loop which will read the sensors, save the data in databas and send it to dweet.io
		:return:
		"""
		while True:
			hum, temp, dist = self.readSensors()
			self.insertDataIntoDatabase(hum, temp)
			self.uploadToDweet(hum, temp, dist)
			time.sleep(1)

	def setTestData(self, _testData):
		self.testData = _testData
	
	def getTestData(self):
		return self.testData
		
	def setTestData1(self, _testData):
		self.testData1 = _testData
	
	def getTestData1(self):
		return self.testData1
		
	def setTestData2(self, _testData):
		self.testData2 = _testData
	
	def getTestData2(self):
		return self.testData2