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

try:
    ser = serial.Serial('/dev/ttyUSB0', 9600)
except NameError:
    pass


class StaticData(object):
    GPIO_DHT = 22

    DHT_HUM_ID = 0
    DHT_TEMP_ID = 1
    DISTANCE_ID = 2

    PROJECT_NAME = "Fluxuskondenzator"
    DWEET_ID = PROJECT_NAME + "_2017"

    DB_HOST = "localhost"
    DB_USERNAME = "root"
    DB_PASSWORD = "root"
    DB_PORT = 3306


class Database(object):
    def __init__(self, connection_data):
        self.__DB_NAME = connection_data['database']
        self.__DB_PASSWORD = connection_data['password']
        self.__DB_USERNAME = connection_data['username']
        self.__DB_HOST = connection_data['host']
        self.__PORT = connection_data['port']

        d = self.conn()
        cur = d[0]
        cur.execute("CREATE TABLE IF NOT EXISTS Datas (sensorTypeID int ,value text, date datetime)")
        cur.execute("CREATE TABLE IF NOT EXISTS SensorTypes (sensorTypeID int, sensorName text)")

        q = "INSERT INTO SensorTypes (sensorTypeID, sensorName) VALUES (" + str(
            StaticData.DHT_HUM_ID) + ", '" + Sensor.STR_HUMIDITY + "')"
        cur.execute(q)
        q = "INSERT INTO SensorTypes (sensorTypeID, sensorName) VALUES (" + str(
            StaticData.DHT_TEMP_ID) + ", '" + Sensor.STR_TEMPERATURE + "')"
        cur.execute(q)
        q = "INSERT INTO SensorTypes (sensorTypeID, sensorName) VALUES (" + str(
            StaticData.DISTANCE_ID) + ", '" + Sensor.STR_DISTANCE + "')"
        cur.execute(q)
        d[1].commit()

    def conn(self):
        """
        Creates connection with the database
        Returns connection and cursor
        :return:
        """
        con = mdb.connect(host=self.__DB_HOST,
                          user=self.__DB_USERNAME,
                          passwd=self.__DB_PASSWORD,
                          db=self.__DB_NAME,
                          port=self.__PORT)
        cur = con.cursor()
        return cur, con

    def getSensorTypeByName(self, name):
        """
        Returns the type of the sensor by name
        :param name:
        :return:
        """
        cur, con = self.conn()
        query = "SELECT sensorTypeID FROM SensorTypes where sensorName='%s'" % (name)
        cur.execute(query)
        type = cur.fetchone()
        try:
            return type[0]
        except TypeError:
            return None

    def getSensorValuesByID(self, id):
        """
        Returns all the values for the Sensor with id
        :param id:
        :return:
        """
        cur, con = self.conn()
        query = "SELECT date, value FROM Datas where sensorTypeID='%s'" % (id)
        cur.execute(query)
        values = cur.fetchall()
        listDatas = []
        for value in values:
            listDatas.append(value)
        return listDatas

    def getSensorLastValueByID(self, id):
        """
        Returns the last value for the sensor with id
        :param id:
        :return:
        """
        cur, con = self.conn()
        query = "SELECT date,value FROM Datas where sensorTypeID='%s' order by date desc" % (id)
        cur.execute(query)
        type = cur.fetchone()
        return type[0], type[1]

    def insertDataBySensorID(self, id, value):
        """
        Insert received or sent messages in the database
        :param id:
        :param value:
        :return:
        """
        cur, con = self.conn()
        query = "INSERT INTO Datas (sensorTypeID, value, date) VALUES ('%s', '%s', NOW())" % (id, value)
        cur.execute(query)
        con.commit()
        return

    def insertDataBySensorName(self, name, value):
        # print name + " " + value
        id = self.getSensorTypeByName(name)
        self.insertDataBySensorID(id, value)


class Sensor(object):
    """
    Sensor
    """
    STR_HUMIDITY = 'Humidity'
    STR_TEMPERATURE = 'Temperature'
    STR_DISTANCE = 'Distance'

    def __init__(self, database):
        self.__database = database

    def readDht(self):
        """
        Reads the data from the DHT sensor
        :return:
        """
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, StaticData.GPIO_DHT)
        return humidity, temperature

    def readSensors(self):
        """
        Reads all the sensors
        :return:
        """
        resp = ""
        try:
            resp = ser.readline()
        except NameError:
            pass
        resp_splitted = resp.split(',')

        hum = 0
        temp = 0
        dist = 0

        for word in resp_splitted:
            if word.find(':') != -1:
                type, data = word.split(':', 1)
                self.__database.insertDataBySensorName(type, data)
                if type == Sensor.STR_HUMIDITY:
                    hum = data
                elif type == Sensor.STR_TEMPERATURE:
                    temp = data
                elif type == Sensor.STR_DISTANCE:
                    dist = data

        return hum, temp, dist


class View(object):
    __dweet = Dweet()

    def __init__(self, database):
        self.__database = database

    def insertDataIntoDatabase(self, hum, temp):
        """
        Inserts the data into the database
        :param hum:
        :param temp:
        :return:
        """
        self.__database.insertDataBySensorID(StaticData.DHT_HUM_ID, hum)
        self.__database.insertDataBySensorID(StaticData.DHT_TEMP_ID, temp)

    def sendData(self, hum, temp, dist):
        """
        Sends the sensor data to dweet.io and returns 'success' on success and 'failed' on failure
        :param hum:
        :param temp:
        :param dist:
        :return:
        """
        try:
            resp = View.__dweet.dweet_by_name(name=StaticData.DWEET_ID, data={Sensor.STR_HUMIDITY: hum,
                                                                              Sensor.STR_TEMPERATURE: temp,
                                                                              Sensor.STR_DISTANCE: dist}
                                              )
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
        print "Sending"
        print "\tHumidity: ", hum
        print "\tTemperature: ", temp
        print "\tDistance: ", dist

        resp = self.sendData(hum, temp, dist)
        print "Result: " + resp + '\n'


def mainLoop():
    """
    Loop which will read the sensors, save the data in databas and send it to dweet.io
    :return:
    """
    connection_data = dict(database=StaticData.PROJECT_NAME,
                           host=StaticData.DB_HOST,
                           username=StaticData.DB_USERNAME,
                           password=StaticData.DB_PASSWORD,
                           port=StaticData.DB_PORT)

    database = Database(connection_data=connection_data)

    sensor = Sensor(database=database)
    view = View(database=database)

    while True:
        hum, temp, dist = sensor.readSensors()
        # insertDataIntoDatabase(hum, temp)
        # sendData(hum, temp)
        view.uploadToDweet(hum, temp, dist)
        time.sleep(1)
