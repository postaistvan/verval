import RPi.GPIO as GPIO
import Adafruit_DHT
import MySQLdb as mdb
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)


def conn():
    con = mdb.connect('localhost', 'root', 'root', 'Fluxuskondenzator')
    cur = con.cursor()
    return cur,con

def getSensorTypeByName(name):
    cur,con=conn()
    query = "SELECT sensorTypeID FROM SensorTypes where sensorName='%s'" % (name)
    cur.execute(query)
    type=cur.fetchone()
    return type[0]

def insertDataBySensorName(name, value):
    print name + " " + value
    id = getSensorTypeByName(name)
    insertDataBySensorID(id,value)
    return


def insertDataBySensorID(id, value):
    """
    Insert received or sent messages in the database
    :param id:
    :param value:
    :return:
    """
    # print id + value
    cur, con = conn()
    # time = dt.now(pytz.utc)
    query = "INSERT INTO Datas (sensorTypeID,value, date) VALUES ('%s', '%s', NOW())" % (id,value)
    cur.execute(query)
    con.commit()
    return


while True:
    test = ser.readline()
    sp = test.split(",")
    for word in sp:
        if word.find(':') !=-1:
            type, data = word.split(':',1)
            insertDataBySensorName(type, data)
