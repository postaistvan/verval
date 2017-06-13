from unittest import TestCase

import MySQLdb
import time

import datetime

from app.src.server import Database, StaticData, Sensor


class TestDatabase(TestCase):

    conn_data = dict(database=StaticData.PROJECT_NAME,
                     host="127.0.0.1",
                     username=StaticData.DB_USERNAME,
                     password=StaticData.DB_PASSWORD,
                     port=3306)

    database = Database(conn_data)

    def test_conn(self):
        database = Database(TestDatabase.conn_data)
        self.assertEqual(type(database.conn()[0]), MySQLdb.cursors.Cursor)
        self.assertEqual(type(database.conn()[1]), MySQLdb.connections.Connection)

    def test_getSensorTypeByName(self):
        r_name = TestDatabase.database.getSensorTypeByName(name=Sensor.STR_DISTANCE)
        self.assertEqual(r_name, StaticData.DISTANCE_ID)

    def test_getSensorValuesByID_is_not_null(self):
        r_v = TestDatabase.database.getSensorValuesByID(id=StaticData.DHT_HUM_ID)
        self.assertTrue(r_v is not None)

    def test_getSensorLastValueByID(self):
        value = 999
        TestDatabase.database.insertDataBySensorID(id=StaticData.DHT_TEMP_ID, value=value)
        r_data = TestDatabase.database.getSensorLastValueByID(id=StaticData.DHT_TEMP_ID)
        # now = datetime.datetime.now()

        self.assertEqual(int(r_data[1]), value)
        # self.assertEqual(r_data[0], now)

    def test_insertDataBySensorID(self):
        test_data = 1
        TestDatabase.database.insertDataBySensorID(StaticData.DHT_HUM_ID, test_data)

        query = "SELECT value FROM Datas where sensorTypeID=0"
        cur = TestDatabase.database.conn()[0]
        cur.execute(query)
        value = cur.fetchone()
        self.assertEqual(int(value[0]), test_data)

    def test_insertDataBySensorName(self):
        test_value = 999
        TestDatabase.database.insertDataBySensorName(name=Sensor.STR_HUMIDITY,
                                                     value=test_value)

        query = "SELECT value FROM Datas where sensorTypeID=" + str(StaticData.DHT_HUM_ID)
        cur = TestDatabase.database.conn()[0]
        cur.execute(query)
        values = cur.fetchall()
        list1 = list()
        for v in values:
            list1.append(int(v[0]))
        self.assertTrue(test_value in list1)
